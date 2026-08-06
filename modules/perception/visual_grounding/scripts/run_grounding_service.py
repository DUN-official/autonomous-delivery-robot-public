import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/grounding_service.local.json")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()
    os.environ["GROUNDING_CONFIG"] = args.config
    import uvicorn
    uvicorn.run(
        "grounding.services.api_service:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )

if __name__ == "__main__":
    main()
