find . \( -name '*.py' -o -name '*.html' \) ! -path "*/__init__.py" ! -path "./env/*" ! -path "./static/*" ! -path "./*/migrations/*" | xargs wc -l | sort -nr