.PHONY: checksetup analysis docs pushv

checksetup:
	conda info --envs \
	&& echo $$(which python)

analysis:
	python3 src/plot.py

docs:
	cd docs \
	&& pandoc --filter pandoc-include --filter pandoc-crossref --citeproc --bibliography=dep/appendix.bib \
		--csl=dep/apa.csl --number-sections --table-of-contents -c dep/empty.css -H dep/custom.css \
		-H dep/plotly.js -H dep/custom.js appendix.md -s -o appendix.html

pushv:
	git tag -a v${version} -m "Bump to Version v${version}" \
	&& git push origin v${version}

all: analysis docs
