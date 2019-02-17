.PHONY: deploy

deploy:
	git push
	ssh dev "cd ~/proj/mem-store && git pull && source venv/bin/activate && pip install -r requirements.txt && mem"
