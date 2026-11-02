from dataclasses import dataclass
from typing import List

@dataclass
class Offer:
    provider: str
    model: str
    input_price: float  # USD per 1M input tokens
    output_price: float  # USD per 1M output tokens
    latency_ms: int

OFFERS: List[Offer] = [
    Offer('ProviderA', 'gpt-4o-mini', 0.15, 0.60, 280),
    Offer('ProviderB', 'gpt-4o-mini', 0.12, 0.55, 410),
    Offer('ProviderC', 'claude-3-haiku', 0.25, 1.25, 190),
    Offer('ProviderD', 'claude-3-haiku', 0.20, 1.10, 260),
    Offer('ProviderE', 'deepseek-chat', 0.14, 0.28, 350),
    Offer('ProviderF', 'deepseek-chat', 0.10, 0.25, 520),
]

def estimate_cost(offer: Offer, in_tokens: int, out_tokens: int) -> float:
    return (in_tokens / 1_000_000) * offer.input_price + (out_tokens / 1_000_000) * offer.output_price

def cheapest(model: str, in_tokens: int = 1000, out_tokens: int = 500, max_latency: int | None = None) -> Offer:
    candidates = [o for o in OFFERS if o.model == model]
    if max_latency is not None:
        candidates = [o for o in candidates if o.latency_ms <= max_latency]
    if not candidates:
        raise ValueError(f'No offer found for {model}')
    return min(candidates, key=lambda o: estimate_cost(o, in_tokens, out_tokens))

def main() -> None:
    model = input('Model [gpt-4o-mini]: ').strip() or 'gpt-4o-mini'
    in_tokens = int(input('Input tokens [1000]: ') or 1000)
    out_tokens = int(input('Output tokens [500]: ') or 500)
    limit = input('Max latency ms [none]: ').strip()
    max_latency = int(limit) if limit else None
    offer = cheapest(model, in_tokens, out_tokens, max_latency)
    cost = estimate_cost(offer, in_tokens, out_tokens)
    print(f'Cheapest: {offer.provider} | {offer.model}')
    print(f'Estimated cost: ${cost:.6f} | latency: {offer.latency_ms}ms')

if __name__ == '__main__':
    main()
