all : \
	perf_rational_baseline.txt \
	perf_rational_big_protocol.txt \
	perf_rational_protocol.txt \
	perf_supports_complex.txt

perf_%.txt : perf_%.ipy Makefile ../numerary/types.py
	ipython --no-banner --quick --LoggingMagics.quiet=True perf_$*.ipy \
		| cut >perf_$*.txt -f 2 -d $$'\a'

../numerary-encumbered.svg : Makefile
	curl --output $@ 'https://img.shields.io/badge/%F0%9F%98%A3-%F0%9D%9A%97%F0%9D%9A%9E%F0%9D%9A%96%F0%9D%9A%8E%F0%9D%9A%9B%F0%9D%9A%8A%F0%9D%9A%9B%F0%9D%9A%A2--encumbered-yellowgreen'
