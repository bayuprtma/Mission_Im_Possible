#!/usr/bin/env python
"""
MissionImPossible CLI - One command ML environments
"""
import argparse
import sys
from missionimpossible import resolve_universal_stack, install_stack

def main():
    parser = argparse.ArgumentParser(description="MissionImPossible ML Resolver")
    parser.add_argument("action", choices=["detect", "resolve", "install", "fix"])
    parser.add_argument("--preset", default="research", 
                       choices=["research", "production", "lightweight"])
    parser.add_argument("--yolo", default="latest", 
                       choices=["latest", "v8", "v10", "v11"])
    parser.add_argument("--gpu", action="store_true")
    parser.add_argument("--framework", choices=["auto", "tensorflow", "pytorch"])
    
    args = parser.parse_args()
    
    if args.action == "detect":
        from missionimpossible import detect_all_conflicts
        print(detect_all_conflicts())
    elif args.action == "resolve":
        result = resolve_universal_stack(
            args.preset, args.yolo, args.gpu, args.framework
        )
        print(result["install_command"])
    elif args.action == "install":
        stack = resolve_universal_stack(args.preset, args.yolo, args.gpu)
        install_stack(stack["preset"])

if __name__ == "__main__":
    main()
