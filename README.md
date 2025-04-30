# PE_KURIAN_SIR – 2-Tier Smart Security System

A Python-based 2-tier security system that detects emergencies from the environment, captures a 12-second video, generates a natural language summary using T5, and sends alerts to the owner (and optionally to neighbors/friends). The system ensures timely response through email and optional WhatsApp API-based notifications.

---

## Repository Link

GitHub: [https://github.com/Gangasagarhl/PE_KURIAN_SIR/](https://github.com/Gangasagarhl/PE_KURIAN_SIR/)

---

##  Setup Instructions

1. **GitHub Access**  
   - If you have a GitHub account, clone the repository:  
     ```bash
     git clone https://github.com/Gangasagarhl/PE_KURIAN_SIR.git
     cd PE_KURIAN_SIR
     ```
   - Otherwise, download the folder from the GitHub page as a ZIP and extract it.

2. **Create a Virtual Environment**  
   ```bash
   python -m venv myenv

3. **Activate a virtual environment**  
   - **Linux/MacOS**:  
     ```bash
     source myenv/bin/activate
     ```  
   - **Windows**:  
     ```bash
     myenv\Scripts\activate
     ```
4. **Run Scripts**
   - pip install -r reuirements.txt
   - python server.py
   - python client.py
