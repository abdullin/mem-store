.PHONY: deploy

deploy:
	git push
	ssh dev "cd ~/proj/mem-store && git pull && mem"
