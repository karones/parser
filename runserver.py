import os, main

port = int(os.environ.get("PORT", 17995))
main.run(debug=True, host='0.0.0.0', port=port)
