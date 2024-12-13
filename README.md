# LlamaLense 🔍🦙

LlamaLense 🔍🦙 is OpenSoure Llama 3.2 RAG app or Chat Bot who answers the questions based on context. **The awesome part of this application is the LLM runs locally!** 🔥  
It takes doc and question as input and returns the answer based on context from the doc. If Question is irrelevant to doc it simply says  "I don't know the answer".

## Pre-requisites & Setup:
**Pre-requisites :**
- Install libmagic based on your OS : [link](https://pypi.org/project/python-magic/#:~:text=This%20module%20is%20a%20simple%20wrapper%20around%20the%20libmagic%20C%20library%2C%20and%20that%20must%20be%20installed%20as%20well)
- Install ollama : [link](https://ollama.com/download)
- We are using `llama3.2:latest`. After installation open terminal and run - `ollama run llama3.2`.
- To check if its running : 
    - Open `http://localhost:11434/` in browser and it should return `Ollama is running`.  
    - OR run this in terminal:  
    ```curl -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{"model": "llama3.2:latest","messages": [{"role": "user", "content": "Hello, what is LLaMA?"}],"stream": false}'```  
    should return LLM response.

**Setup instructions :**
- Clone this repository.
- `cd llamalens`.
- Create venv : `python3 -m venv ll_venv`.
- Activate venv : `source ll_venv/bin/activate`.
- Install `requirement.txt` : `pip3 install -r requirements.txt`.
- To Run in **Terminal** :
    - Run `llamalense.py` file in venv : `~/llamalens/ll_venv/bin/python ~/llamalens/llamalense.py`.
    - User `--log_level DEBUG` option incase you want all outputs.
- To Run using **UI** :
    - Start backend : `python3 -m uvicorn backend.api:app --reload`.
    - Launch frontend : open `~/llamalens/frontend/index.html` locally in your browser. 
    - Make sure backend is running on `http://127.0.0.1:8000` or change in `~/llamalens/frontend/index.html` if different.


## Docs :  
- [End-To-End MLOps Pipeline](/docs/End-To-End%20MLOps%20Pipeline.md)
- [Performance Evaluation Methods](/docs/Performance%20Evaluation%20Methods.md)
- [Pipeline Management](/docs/Pipeline%20Management.md)

## Terminal Run Outputs (Without UI) :
**DOCX :**  

![image](/outputs/terminal_run/docx-output.png)

**PDF :**  

![image](/outputs/terminal_run/pdf-output.png)

## UI Output :
**DOCX :**  

![image](/outputs/ui_run/docx-output.png)


**PDF :**  

![image](/outputs/ui_run/pdf-output.png)

