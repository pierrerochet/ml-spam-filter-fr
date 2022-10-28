# Spam filter with machine learning

<!-- ![email](./images/email.png) -->

<figure>
  <img src="./assets/email.png" alt="email"/>
  <figcaption style="text-align: center;"><i>Image par <a href="https://pixabay.com/fr/users/tumisu-148124/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2362038">Tumisu</a></i></figcaption>
</figure>

## 🔥 Objective and motivation

Build a **spam filter** with **machine learning** for **french**.

The fight against spamming is both one of the oldest computer security problems and one that has been successfully solved through machine learning.

Thinking and building such a system is a rewarding experience for those interested in applying machine learning to computer security. This project therefore has a mainly **educational purpose**.

## 📚 Tools and knowledge

### 🛠 Tools

- [Sklearn](https://scikit-learn.org/stable/) - A python library to traditionnal machine-learning
- [FastAPI](https://fastapi.tiangolo.com/) - A python micro framework to build API fastly

### 📖 Knowledge

- Python development skill
- [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) for text vectorization
- [Linear Support vector machine](https://en.wikipedia.org/wiki/Support_vector_machine) (LinearSVM) and [Stochastic Gradient Descent](https://en.wikipedia.org/wiki/Stochastic_gradient_descent) (SGD) for model training
- API develpement to serve the model

## 🧬 Project structure

```
├── README.md
├── app
│   ├── main.py
│   └── ml_models
├── data
│   └── data-en-hi-de-fr.csv
├── notebooks
│   └── build-model.ipynb
└── requirements.txt
```

| Folder    | Description                                                          |
| --------- | -------------------------------------------------------------------- |
| app       | api source code                                                      |
| ml_models | machine-learning models trained and load when the application starts |
| data      | data used during training                                            |
| notebooks | contains the notebooks for data manipulation and model training      |

## 🔑 How use it

### 🔗 Install dependencies

```bash
pip install -r requirements.txt
```

Note - We recommand do it in a vitual environment.

### 🚀 Start the API

```bash
uvicorn app.main:app
```

The documentation can be reached at this url http://127.0.0.1:8000/docs

### ✨ Resquest example

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/verify' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Vous avez gagnez un cadeau ! Recevez votre gain en cliquant ici !"
}'
```

will return

```json
{
  "is_spam": true,
  "confidence": 0.921,
  "input_text": "Vous avez gagnez un cadeau ! Recevez votre gain en cliquant ici !",
  "time": "2022-10-26 17:07:04"
}
```

## 💎 Data used in the project

You can dowload them on [Kaggle](https://www.kaggle.com/datasets/rajnathpatel/multilingual-spam-data?resource=download)  
Author - [Raj Nath Patel](https://www.kaggle.com/rajnathpatel)

These are 5134 french text from emails spliiting into 3593 for training and 1541 for testing (30 %).

The original text was in English and Machine Translated to French. The dataset therefore contains some inconsistencies in meaning due to translation errors.

The data only provides the body of the email in raw text, which means that we do not have the sender email addresses or any other metadata.

Below a exemple:

> "En tant que client apprécié, je suis heureux de vous informer qu'à la suite d'un récent examen de votre Mob No. vous êtes récompensé avec un Prix Bonus £1500, appelez 09066364589"

## 📈 Performances

|      | precision | recall | f1-score | support |
| ---- | --------- | ------ | -------- | ------- |
| ham  | 0.99      | 1.00   | 0.99     | 1349    |
| spam | 0.98      | 0.91   | 0.94     | 192     |

Note - The **test data is 30%** of the total data.

## 💡 Choices made in the project

Here we tried to respond most frequently questions and justify choices made in the project.

### _Why a spam filter for French language ?_ 🇫🇷

Because French is a beautiful language 😉

### _Why use a linear SVM and Stochastic Descent Gradient for model training ?_

Historically, LinearSVM performs well on large datasets for relatively fast training time. It is therefore particularly suitable for textual data.

We selected it for its good performance compared to the other algorithms we tested.

Using SGD for convergence allows us iterative learning. This strategy is useful for updating our model with new observations (see [partial_fit](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html#sklearn.linear_model.SGDClassifier.partial_fit)).

The performances are good enough not to consider heavier architectures based on neural networks. In addition, we have chosen to favor a light and easy to handle model.

### _Why do a probability calibration? ?_

> When performing classification you often want not only to predict the class label, but also obtain a probability of the respective label. This probability gives you some kind of confidence on the prediction. Some models can give you poor estimates of the class probabilities and some even do not support probability prediction (e.g., some instances of SGDClassifier). The calibration module allows you to better calibrate the probabilities of a given model, or to add support for probability prediction.
>
> -- [_Sklearn documentation_](https://scikit-learn.org/stable/modules/calibration.html)

Although not required, we want a **confidence score** in order to **manage the filter strength** in the service.

### _Why use FastAPI to build the API ?_

> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
>
> -- [_FastAPI Documentation_](https://fastapi.tiangolo.com/)

FastAPI is the python framework allowing to build API **fastest**.

**Easy to learn, based on standard python type, automatically generates the documentation** are some of its many advantages.

For building ML service in python it has become a standard choice in many projects.

## How to improve the project ?

First, the use of native French data could improve post-deployment spam detection.

Another good option will be to found email dataset with additional elements such as sender address, url, html code, attachments, etc. We believe that these elements should allow to build very good features to discriminate spams.

Depending on the elements, other algorithms would be required for training. For example, more complex methods based on neural networks should work better for inspecting attachements.

Combining these improvements could make a very powerful anti spam. But the project would also be much more difficult.

# Author

[Pierre ROCHET](https://github.com/pierrerochet)
