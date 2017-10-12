#!/usr/local/bin/python3
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scrape import app

if __name__ == '__main__':
	sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
	if len(sys.argv) > 1:
		cmd = sys.argv[1]
		if cmd == 'test' or cmd == 'once':
			sys.exit(app.run_once())
	sys.exit(app.main())