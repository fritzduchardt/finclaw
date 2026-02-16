# Wikipedia

## Extract
```bash
curl "https://en.wikipedia.org/w/api.php?action=query&titles=DevOps&prop=extracts&exintro&explaintext&format=json" | jq
```

## Info
```bash
curl "https://en.wikipedia.org/w/api.php?action=query&titles=DevOps&prop=info&format=json" | jq
```
