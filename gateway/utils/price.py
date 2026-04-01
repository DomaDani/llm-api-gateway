from genai_prices import Usage, calc_price
from shared.config import PROVIDER_ID, DEFAULT_INPUT_MTOKEN_PRICE, DEFAULT_OUTPUT_MTOKEN_PRICE

def calculate_cost(usage: Usage, model_ref: str, provider_id: str) -> float:
    try:
        cost = calc_price(
            usage=usage,
            model_ref=model_ref,
            provider_id=provider_id
        ).total_price
    except Exception as e:
        cost = (usage.input_tokens / 1_000_000) * DEFAULT_INPUT_MTOKEN_PRICE + (usage.output_tokens / 1_000_000) * DEFAULT_OUTPUT_MTOKEN_PRICE
        print(f"WARNING: Price calculation failed with error: {e}. Falling back to default pricing. Estimated cost: ${cost:.6f}")
    
    return cost