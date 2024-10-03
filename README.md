# Streamlit Authenticator with Roles

Streamlit Authentication Template with Roles! Start by adding a component python script & 3 line of code.

## 🔨 Getting Started

### 1. Install dependencies

    ```
    pip install -r requirements.txt
    ```

### 2. Run application by

    ```
    streamlit run app.py
    ```

## ✨ Adding to your project

### 1. Copy required files as:

```bash
project_dir/
|___ component/
| |___ authentication.py  # copy from this project
|___ my_pages/            # default subpage is "my_pages"
| |___ page1.py  
| |___ page2.py  
```
### 2. Initialize the authentication component

```python
# Add these 3 lines to the main script
import component
from component import authentication

authentication.init_authentication("credentials.yml", subpage_path="my_pages")

# Keep here empty
```

### 3. Update credential configuration

```yaml
# path located at: 
roles:
  admin:
    page_restrictions: null
  user: 
    page_restrictions: 
      - page1
```

### 4. Done! Launch the app and try it!


## 📃 Reference

- [Streamlit Blog](https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/)
- [Streamlit-Authenticator (Github)](https://github.com/mkhorasani/Streamlit-Authenticator)
