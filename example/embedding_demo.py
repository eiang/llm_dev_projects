import numpy as np
from fastembed import TextEmbedding

model = TextEmbedding(
    model_name="BAAI/bge-small-zh-v1.5"
)

texts = [
    "P1级生产事故需要在15分钟内响应。",
    "最高等级线上事故需要尽快处理。",
    "今天中午我想吃一碗牛肉面。",
]

embeddings = model.embed(texts)

print(type(embeddings))

vectors = list(embeddings)

print(type(vectors))
print(len(vectors))

print(vectors[0].shape)
print(vectors[1].shape)
print(vectors[2].shape)


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


score_01 = cosine_similarity(
    vectors[0],
    vectors[1],
)

score_02 = cosine_similarity(
    vectors[0],
    vectors[2],
)

print("句子1 vs 句子2:", score_01)
print("句子1 vs 句子3:", score_02)

a = np.array([1, 1])
b = np.array([2, 2])

dot_result = np.dot(a, b)

print("dot:", dot_result)
print("a norm:", np.linalg.norm(a))
print("b norm:", np.linalg.norm(b))


a = np.array([1, 1])
b = np.array([2, 2])

c = np.array([1, 0])
d = np.array([0, 1])

e = np.array([1, 1])
f = np.array([-1, -1])

print("a vs b:", cosine_similarity(a, b))
print("c vs d:", cosine_similarity(c, d))
print("e vs f:", cosine_similarity(e, f))

documents = [
    "员工每年有10天带薪年假。",
    "P1级生产事故需要在15分钟内响应。",
    "生产环境发布必须经过Code Review。",
]
query = "线上最高等级事故多久必须响应？"

query_vector = list(
    model.embed([query])
)[0]

document_vectors = list(
    model.embed(documents)
)
results = []
for index, document in enumerate(documents):
    score = cosine_similarity(
        query_vector,
        document_vectors[index],
    )

    results.append(
        {
            "document": document,
            "score": score,
        }
    )
print(results)