# API Testing Guide

## Using curl

### Text Search
```bash
curl -X POST http://localhost:8000/api/search/text/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "iPhone 15 Pro",
    "platforms": ["jumia", "amazon"],
    "max_results": 10
  }'
```

### Check Search Status
```bash
curl http://localhost:8000/api/search/status/<task_id>/
```

### Image Search
```bash
curl -X POST http://localhost:8000/api/search/image/ \
  -F "image=@product.jpg" \
  -F "max_results=20"
```

### Compare Products
```bash
curl http://localhost:8000/api/compare/?query=iPhone+15
```

### List Products
```bash
curl http://localhost:8000/api/products/
```

### Get Product Details
```bash
curl http://localhost:8000/api/products/1/
```

### Get Price History
```bash
curl http://localhost:8000/api/products/1/price_history/
```

## Using Python

```python
import requests

# Text search
response = requests.post('http://localhost:8000/api/search/text/', json={
    'query': 'Samsung Galaxy S24',
    'platforms': ['jumia', 'kilimall', 'amazon'],
    'max_results': 20
})
result = response.json()
task_id = result['task_id']

# Check status
import time
while True:
    status = requests.get(f'http://localhost:8000/api/search/status/{task_id}/').json()
    if status['status'] == 'completed':
        products = status['products']
        break
    time.sleep(2)

# Compare products
compare = requests.get('http://localhost:8000/api/compare/', params={
    'query': 'Samsung Galaxy S24'
}).json()
```

## Using JavaScript

```javascript
// Text search
const response = await fetch('http://localhost:8000/api/search/text/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'MacBook Pro',
    platforms: ['amazon', 'ebay'],
    max_results: 20
  })
});
const result = await response.json();

// Poll for results
const checkStatus = async (taskId) => {
  const response = await fetch(`http://localhost:8000/api/search/status/${taskId}/`);
  return response.json();
};

let status;
do {
  status = await checkStatus(result.task_id);
  await new Promise(resolve => setTimeout(resolve, 2000));
} while (status.status !== 'completed');

console.log(status.products);
```
