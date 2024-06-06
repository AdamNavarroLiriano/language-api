# Language Translation API

## Project Overview

This project aims to create a Language Translation API based on Machine Learning. Currently, the API supports translations for four language pairs:
- Danish - English (da-en)
- English - Danish (en-da)
- English - Swedish (en-sv)
- Swedish - English (sv-en).

Our immediate goal is to expand the API to support up to 12 language pairs, adding support for Norwegian Bokmål (nb), and allowing for translations in all possible combinations of language pairs in the set {da, en, nb, sv}.

## Getting Started

To use this project, follow these steps:

1. Clone the repository by running this command in your terminal:

```bash
git clone https://github.com/AdamNavarroLiriano/language-api
```

2. After the repository is cloned, initialize the server running the follwoing command:

```bash
docker compose up --build
```

Once the setup is complete, our Language Translation API will be up and running, as a default on port 80 of your localhost. You can access the API documentation at http://localhost/docs.

To interact with the API, you must send POST requests to the /translate/sentence/ endpoint. Here's an example of how to translate "Hello, world!" from English to Swedish using the API:

```bash
curl -X 'POST' \
  'http://localhost/translate/sentence/?src_text=Hello%2C%20world%21&src=en&tgt=sv' \
  -H 'accept: application/json' \
  -d ''
```

The API will respond with:

```json
{
  "status_code": 200,
  "response": "Hallå, världen!"
}
```

## Development Approach

We used both pretrained models and finetuned models, based on the [Marian](https://huggingface.co/docs/transformers/en/model_doc/marian) family of models for Machine Translation. In particular
* Language pairs en-da, da-en, and sv-en leverage pretrained models. 
* For en-sv pair, we trained a specialized model based on the checkpoint available at HuggingFace as of June 2024. Finetuning was performed at kaggle and code is avaiable at [`notebooks/1-EDA.ipynb`](./notebooks/2-finetune.ipynb)
 
All models were evaluated using the BLEU metric, implemented via the [sacrebleu](https://github.com/mjpost/sacrebleu) python package.

## Data Analysis

We performed Exploratory Data Analysis (EDA) in [`notebooks/1-EDA.ipynb`](./notebooks/1-EDA.ipynb). The key findings of this analysis include:

- The number of observations for each language pair in the training data varies between 89K and 158K.
- Danish (da) had the highest number of translations as both a source and target language, while English (en) has the lowest amount of observations.
- English (en) and Swedish (sv) had the smallest amount of observations as source language.
- Texts in the da-en language pair were generally shorter than the rest of the 11 pairs.
- There are four language pairs (en-nb, sv-da, da-sv, nb-en) which are not supported by pretrained models from the MarianMT model family.
- In HuggingFace, Norwegian Bokmål (nb) is not generally supported for Machine Translation tasks, limiting its interaction with other languages. As a substitue, we can use the 'no' language code, and some language pairs will be available.
- Using pretrained models from the this model family, the language pairs da-en and en-da have the highest BLEU score.
- The lowest performing models all have Norwegian Bokmål (nb) as either the source language or target language.
- Apart from languages with **`nb`** interaction, the language pair en-sv has the lowest performing model, and it's BLEU score is significantly lower than its counterpart language pair sv-en, which has the third highest BLEU score out of all models.

## Scaling and Optimization

Scaling up the training process may require the use of specialized hardware such as GPUs and TPUs, possibly in a distributed manner. Such specialized software can also be used at inference time to improve the API's latency response.

Smaller models (by distilling the models), different architectures or quantization can also be used to reduce memory usage and speed up inference. The trade-off would be the quality of the output, and therefore a decrease in the BLEU metric.  

Asynchronous processing can aid in handling multiple requests simultaneously. Storing models in an accessible way can help avoid repeated downloads, thereby improving latency time and unnecessary processing tasks. 

Investigating autoscaling with Kubernetes can be beneficial, as we could potentially scale up the service when there's a lot of traffic.

## Making the API Production-Ready

Before deploying the API for production use, it's crucial to implement security features such as authentication and authorization. HTTPS protocol should be adopted for secure communication over the internet.

Container orchestration can help scale the service based on load and model complexity. Asynchronous programming, hardware optimization, and efficient model loading can enhance latency.

There are other software engineering practices that ought to be implemented such as unit testing and integration testing. This gives confidence in the workings of the software and their interactions. Additionally, it can serve as documentation for future developers working on the product.

From an ethical standpoint, the quality of the models' output should be monitored to ensure the accuracy and fairness of translations.

## Roadmap and Future Scope

To further expand and improve the MT system, consider using larger and more diverse datasets for training, such as the ones listed [here](https://metatext.io/datasets-list/translation-task). One might also consider pairing subtitles and closed-captions for same content on different languages. Whenever possible, pairing information from the web is possible through webscraping.

The use of pretrained or multilingual models can expedite the training process, and serve as an initial base to support more language pairs.

An strategic roadmap for the product looks as follow:
1. Introduce authentication and authorization, and enable HTTPS on the container. This is necessary for security reasons.
2. Deploy on a container services (Amazon ECS, Azure Containers, etc.) and add logging to monitor usage. We would get a sense on the traffic and prioritize aspects such as improving inference, availabilty, scaling and concurrency.
3. Having a working product, next task is to expand the translation services for all 12 language pairs in the combination set (da, en, nb, sv). This can be done as follows:
   1. Using pretrained models, the models with highest BLEU scores can be made available already.
   2. Simmultaneously, the models can be finetuned with the current dataset to improve their performance.
   3. Afterwards, models from scratch need to be trained for the pairs which are not currently supported.
4. Expand to different language pairs.
     * Priorization can be done based on a product framework such as RICE (Reach, Impact, Confidence, Effort) or MoSCoW (Must-Have, Should-Have, Could-Have, Won't-Have).
     * Ideally, we would like to add support to combinations of languages that are impactful and where there's a solid starting base (e.g. English-Spanish, Spanish-English). However, the vision of the product and the market it is aimed to cover is a great consideration.
5. Add extra features and customization, to increase the reach of the product.
     * For example, there could be models which are aimed at subtitles generation, advertisement, literature or even aid the translation of judicial documents.