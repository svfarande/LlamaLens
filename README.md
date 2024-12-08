# QuestionsPro Bot 

This is simple RAG app or Chat Bot who answers the questions based on context. It takes doc and question as input and returns the answer based on context from the doc. If Question is irrelevant to doc it simply says  "I don't know the answer".

## Pre-requisites & Setup:
**Pre-requisites :**
- Install libmagic based on your OS : [link](https://pypi.org/project/python-magic/#:~:text=This%20module%20is%20a%20simple%20wrapper%20around%20the%20libmagic%20C%20library%2C%20and%20that%20must%20be%20installed%20as%20well)
- Install ollama : [link](https://ollama.com/download)
- We are using `llama3.2:latest`. After installation open terminal and run - `ollama run llama3.2`
- To check if its running : 
    - open `http://localhost:11434/` in browser and it should return `Ollama is running`  
    - Or run this in terminal:  
    ```curl -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{"model": "llama3.2:latest","messages": [{"role": "user", "content": "Hello, what is LLaMA?"}],"stream": false}'```  
    should return LLM response.

**Setup instructions :**
- Clone this repository
- `cd qp-ai-assessment`
- Create venv : `python3 -m venv qp_bot_venv`
- Activate venv : `source qp_bot_venv/bin/activate`
- Install `requirement.txt` : `pip3 install -r requirements.txt`
- Run `qpbot.py` file in venv : `~/qp-ai-assessment/qp_bot_venv/bin/python ~/qp-ai-assessment/qpbot.py`
- User `--log_level DEBUG` option incase you want all outputs.

## Docs :
- [End-To-End MLOps Pipeline](/docs/End-To-End%20MLOps%20Pipeline.md)
- [Performance Evaluation Methods](/docs/Performance%20Evaluation%20Methods.md)
- [Pipeline Management](/docs/Pipeline%20Management.md)

## Outputs :
**DOCX :**
![image](/outputs/docx%20output.png)

**PDF :**
![image](/outputs/pdf%20output.png)
