ROADMAP = {
    "Python": "Practice variables, functions, collections, file handling, and small automation projects.",
    "SQL": "Learn SELECT, filtering, joins, grouping, subqueries, and practice with a small database.",
    "Excel": "Practice formulas, lookup functions, pivot tables, charts, and data cleaning.",
    "Pandas": "Work with DataFrames, missing values, grouping, merging, and CSV datasets.",
    "Power BI": "Build a dashboard using a sample dataset and practice data modelling and DAX basics.",
    "Machine Learning": "Study supervised learning, train/test split, evaluation metrics, and build a small model.",
    "scikit-learn": "Practice preprocessing, pipelines, model training, cross-validation, and evaluation.",
    "FastAPI": "Create a small REST API with request models, validation, and prediction endpoints.",
    "Docker": "Containerize a simple Python application and learn images, containers, and Dockerfiles.",
    "Deep Learning": "Learn neural-network basics and implement a small model using a beginner-friendly framework.",
    "LLM": "Understand tokens, prompting, model limitations, and build a small LLM-powered prototype.",
    "RAG": "Learn embeddings, chunking, vector search, retrieval, and grounded answer generation.",
    "APIs": "Learn HTTP methods, JSON, status codes, authentication basics, and API testing.",
    "NLP": "Practice tokenization, text cleaning, TF-IDF, embeddings, and text classification.",
    "Transformers": "Understand attention and transformer encoders; fine-tune or use a pretrained model.",
    "Hugging Face": "Explore the Transformers library and run a pretrained text-classification pipeline.",
    "OpenCV": "Practice image loading, resizing, color spaces, filtering, and basic object detection.",
    "CNN": "Learn convolution, pooling, and train a small image classifier.",
    "YOLO": "Run a pretrained YOLO detector and evaluate it on a small set of sample images.",
    "Git": "Practice commits, branches, merges, and pushing a project to GitHub.",
    "Linux": "Practice shell navigation, file permissions, processes, and common command-line tools.",
    "Statistics": "Revise distributions, averages, variance, hypothesis testing, and correlation.",
    "Data Visualization": "Create clear plots and dashboards; explain the insight behind each chart."
}

def generate_roadmap(missing_skills):
    roadmap = []
    for index, skill in enumerate(missing_skills, start=1):
        action = ROADMAP.get(skill, f"Study the fundamentals of {skill} and complete one small practical project.")
        roadmap.append({"week": f"Week {index}", "skill": skill, "action": action})
    return roadmap
