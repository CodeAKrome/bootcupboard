sample:
	cat sample.jsonl| jq .text | python x_gemkey.py system5.txt | sed "s/\'/\\\'/g" | sed "s/’/\\'/g" | sed "s/'/\\'/g" |  egrep CREATE | sed 's/CREATE/MERGE/g' > sample.cypher
sample2:
	cat sample2.jsonl| jq .text | python x_gemkey.py system7.txt | grep MERGE > sample2.cypher
gemini:
	litellm --model gemini/gemini-1.5-flash
geminiexp:
	litellm --model gemini/gemini-1.5-pro-exp-0827
