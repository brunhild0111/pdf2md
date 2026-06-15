import argparse
import os
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "marker").is_dir():
            return p
    return start.parents[0]


repo_root = _find_repo_root(Path(__file__).resolve())
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))


def main():
    parser = argparse.ArgumentParser(
        description="Convert a single PDF to Markdown using Marker"
    )
    parser.add_argument(
        "--pdf",
        type=str,
        default="E-DBSCAN.pdf",
        help="Path to the input PDF file",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Directory to save output (defaults to settings.OUTPUT_DIR)",
    )
    parser.add_argument(
        "--page_range",
        type=str,
        default=None,
        help="Pages to process, e.g. '0,5-10,20'",
    )
    parser.add_argument(
        "--force_ocr",
        action="store_true",
        help="Force OCR on all pages",
    )
    parser.add_argument(
        "--paginate_output",
        action="store_true",
        help="Insert page separators in markdown",
    )
    parser.add_argument(
        "--use_llm",
        action="store_true",
        help="Use LLM-enhanced processors",
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["auto", "cpu", "cuda"],
        default="cuda",
        help="Compute device for models (auto/cpu/cuda)",
    )
    parser.add_argument(
        "--dtype",
        type=str,
        choices=["auto", "float32", "float16", "bfloat16"],
        default="auto",
        help="Precision for models (auto/float32/float16/bfloat16)",
    )
    parser.add_argument(
        "--attention",
        type=str,
        choices=["auto", "sdpa"],
        default="auto",
        help="Attention implementation hint (auto/sdpa)",
    )

    args = parser.parse_args()

    try:
        from marker.models import create_model_dict
        from marker.config.parser import ConfigParser
        from marker.output import save_output
        from marker.logger import configure_logging, get_logger
    except ModuleNotFoundError:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        from marker.models import create_model_dict
        from marker.config.parser import ConfigParser
        from marker.output import save_output
        from marker.logger import configure_logging, get_logger

    configure_logging()
    logger = get_logger()

    config: dict = {}
    if args.output_dir:
        config["output_dir"] = args.output_dir
    if args.page_range:
        config["page_range"] = args.page_range
    if args.force_ocr:
        config["force_ocr"] = True
    if args.paginate_output:
        config["paginate_output"] = True
    if args.use_llm:
        config["use_llm"] = True

    config_parser = ConfigParser(config)

    device = None
    dtype = None
    attention = None
    try:
        import torch

        if args.device == "cuda" or (args.device == "auto" and torch.cuda.is_available()):
            device = "cuda"
        else:
            device = "cpu"

        if args.dtype == "auto":
            dtype = torch.float16 if device == "cuda" else None
        elif args.dtype == "float16":
            dtype = torch.float16
        elif args.dtype == "bfloat16":
            dtype = torch.bfloat16
        elif args.dtype == "float32":
            dtype = torch.float32

        attention = None if args.attention == "auto" else args.attention
    except Exception:
        device = None
        dtype = None
        attention = None

    models = create_model_dict(device=device, dtype=dtype, attention_implementation=attention)

    converter_cls = config_parser.get_converter_cls()
    converter = converter_cls(
        config=config_parser.generate_config_dict(),
        artifact_dict=models,
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service(),
    )

    rendered = converter(args.pdf)
    out_folder = config_parser.get_output_folder(args.pdf)
    base_name = config_parser.get_base_filename(args.pdf)

    os.makedirs(out_folder, exist_ok=True)
    save_output(rendered, out_folder, base_name)
    logger.info(f"Saved markdown to {out_folder}")


if __name__ == "__main__":
    main()

