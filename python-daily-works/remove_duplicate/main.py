import argparse
import sys

def remove_duplicates(input_file, output_file=None):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Use a set to check for duplicates and a list to maintain original order
        seen = set()
        unique_lines = []
        removed_values = []
        
        for line in lines:
            # Strip whitespace and newline characters
            clean_line = line.strip() 
            
            # Skip empty lines
            if clean_line == "":
                continue
                
            if clean_line not in seen:
                seen.add(clean_line)
                unique_lines.append(clean_line)
            else:
                # Track the duplicate values that are being removed
                # We check if it's already in removed_values to avoid listing the same value multiple times
                if clean_line not in removed_values:
                    removed_values.append(clean_line)
        
        # --- Print summary of removed duplicates ---
        print("-" * 30)
        if removed_values:
            print(f"🗑️  Removed duplicate values: {', '.join(removed_values)}")
        else:
            print("✨ No duplicate values found.")
        print("-" * 30)

        # --- Handle output ---
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in unique_lines:
                    f.write(item + '\n')
            print(f"✅ Success! Output saved to: {output_file}")
        else:
            print("📄 Unique content:")
            for item in unique_lines:
                print(item)

    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.", file=sys.stderr)
    except Exception as e:
        print(f"❌ Unknown error: {e}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool to remove duplicate lines from a text file.")
    parser.add_argument("input", help="Path to the input file")
    parser.add_argument("-o", "--output", help="Path to the output file (optional). If not provided, prints to console.", default=None)
    
    args = parser.parse_args()
    
    remove_duplicates(args.input, args.output)