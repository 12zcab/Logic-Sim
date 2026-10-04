import os
import sys
import traceback
import pkgutil
if __name__ == '__main__':
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.abspath(os.path.join(base_dir, 'Source'))
    external_app = os.path.join(source_dir, 'app.py')
    
    if os.path.exists(external_app):
        sys.path.insert(0, source_dir)
        sys.argv = [external_app] + sys.argv[1:]
        try:
            with open(external_app, 'r', encoding='utf-8') as f:
                code = f.read()
            global_env = {
                '__name__': '__main__',
                '__file__': external_app,
                '__builtins__': __builtins__
            }
            exec(code, global_env)
            
        except Exception as e:
            print("\n" + "="*50)
            print("  APPLICATION CRASH DETECTED  ")
            print("="*50 + "\n")
            traceback.print_exc()
            print("\n" + "="*50)
            input("\nPress Enter to close...")
    else:
        print(f"Error: '{external_app}' not found.")
        input("Press Enter to exit...")
