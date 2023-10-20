
# Article Analyzer Installation Guide

## Prerequisites

- Ensure that you have `minikube` installed and running on your Unix-based environment.

## Installation Steps

1. **Set up the Minikube Docker environment**:
   This step ensures that you are building the Docker image directly in Minikube's Docker environment.

    ```bash
    eval $(minikube docker-env)
    ```

2. **Build the Docker image**:
   Navigate to the directory where your `Dockerfile` resides and execute the following command to build the Docker image.

    ```bash
    sudo docker build -t article_analyzer .
    ```

3. **Deploy the application using Kubernetes**:
   This step will deploy the application using the provided Kubernetes configuration file.

    ```bash
    kubectl create -f ./article_analyzer.yaml
    ```

4. **Port-forward the application**:
   This will forward the port from the Kubernetes pod to your local machine.
   ## NOTE: 
   Alternatively, this could have been done with exposing the Pod as a Kubernetes Service.
   Using a Load Balancer, assuming you cloud provider supports load balancers.
   However, for this case, I try to make it as simple as possible, so I just use port forward 

    ```bash
    kubectl port-forward my-fastapi-app :80
    ```

    Note: This command will display the local port being used, e.g., `Forwarding from 127.0.0.1:XXXXX -> 80`. Take note of this port.

5. **Access the application**:
   Open your web browser and navigate to:

    ```
    http://localhost:XXXXX
    ```

   Replace `XXXXX` with the port number displayed in the previous step.

## Conclusion

That's it! You should now be able to see and interact with the Article Analyzer application in your web browser.

-------------------------------------------------------------------------------------------------------


---

# Development Process Explanation for Article Analyzer

The Article Analyzer is a FastAPI application that displays articles and their most common words. Articles are stored in text files inside the `./articles` folder in the project root. The HTML template `index.html` is located in the `./templates` folder in the project root.

## Structure

- Articles are stored as text files in the `./articles` folder.
- The HTML template `index.html` is stored in the `./templates` folder.

## `index.html` Overview

The `index.html` file is an HTML document that uses [HTMX](https://htmx.org/) to handle asynchronous requests. It displays a list of articles and provides a button to find the most common words for each article. When the button is clicked, HTMX sends a POST request to fetch and display the common words without reloading the page.

## `app.py` Overview

The `app.py` file contains the FastAPI application logic.

### Main Components:

1. **Logger:**
   A logger is set up for debugging purposes. It helps to verify if the LRU cache is working and fetching data from the cache instead of reading from files every time.

   ```python
   logging.basicConfig(level=logging.INFO)
   ```

2. **Stop Words:**
   A set of common English words that should be excluded from the common words analysis.

   ```python
   STOPWORDS = {...}
   ```

3. **LRU Cache:**
   The `get_article_content` function uses an LRU cache to store the content of articles. This improves performance by avoiding repeated file read operations.

   ```python
   @lru_cache(maxsize=None)
   def get_article_content(article_name: str) -> str:
   ```

### Main Endpoints:

1. **`/` (GET):**
   Displays the list of articles.

   ```python
   @app.get("/", response_class=HTMLResponse)
   ```

2. **`/article/{article_name}` (GET):**
   Displays the content of a specific article.

   ```python
   @app.get("/article/{article_name}", response_class=HTMLResponse)
   ```

3. **`/process-article/{article_name}` (POST):**
   Analyzes the content of a specific article and returns the most common words.

   ```python
   @app.post("/process-article/{article_name}")
   ```

## Conclusion

The Article Analyzer is a simple FastAPI application that demonstrates the use of HTMX for asynchronous web requests, LRU caching for performance improvement, and basic text analysis to find common words in articles. The logger in place helps to verify the efficiency of caching.

---
