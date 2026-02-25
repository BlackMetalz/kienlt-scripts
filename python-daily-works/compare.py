import argparse
import sys
from pathlib import Path

def process_file(file_path: str, case_sensitive: bool) -> set[str]:
    """
    Read a file, trim whitespace, remove empty lines, and normalize text case.
    
    Args:
        file_path: Path to the file to process
        case_sensitive: If False, converts all text to lowercase for comparison
        
    Returns:
        A set of unique non-empty lines from the file
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
        
    lines = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            cleaned = line.strip()
            if not cleaned:
                continue
            
            # For case-insensitive comparison, convert to lowercase
            if not case_sensitive:
                cleaned = cleaned.lower()
                
            lines.add(cleaned)
    return lines

def main():
    parser = argparse.ArgumentParser(
        description="Compare two text files and identify lines from the first file that are not present in the second file.",
        epilog="Example: python compare.py file1.txt file2.txt --case-sensitive"
    )
    
    # Two required arguments (made optional to allow --help without arguments)
    parser.add_argument("file_1", nargs='?', help="First file to compare (source)")
    parser.add_argument("file_2", nargs='?', help="Second file to compare (reference)")
    
    # Optional argument for Case Sensitivity
    parser.add_argument(
        "-c", "--case-sensitive", 
        action="store_true",
        help="Enable case-sensitive comparison (default: case-insensitive)"
    )

    args = parser.parse_args()

    # Show help if no files are provided
    if not args.file_1 or not args.file_2:
        parser.print_help()
        sys.exit(0)

    # Process data from both files
    set_1 = process_file(args.file_1, args.case_sensitive)
    set_2 = process_file(args.file_2, args.case_sensitive)

    # Find lines in file_1 but not in file_2
    missing = set_1 - set_2

    # Results summary
    print(f"{'='*60}")
    print("Comparison Result")
    print(f"{'='*60}")
    print(f"Source File (File 1):    {args.file_1}")
    print(f"Reference File (File 2): {args.file_2}")
    print(f"Comparison Mode:         {'Case-Sensitive' if args.case_sensitive else 'Case-Insensitive'}")
    print(f"{'='*60}\n")

    if not missing:
        print("✓ All lines from File 1 are present in File 2.")
    else:
        print(f"✗ Found {len(missing)} line(s) in File 1 that are NOT present in File 2:\n")
        # Print the list sorted for better readability
        for i, item in enumerate(sorted(missing), 1):
            print(f"  {i}. {item}")

if __name__ == "__main__":
    main()
