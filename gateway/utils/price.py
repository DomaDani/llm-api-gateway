from genai_prices import Usage, calc_price
from shared.config import PROVIDER_ID, DEFAULT_INPUT_MTOKEN_PRICE, DEFAULT_OUTPUT_MTOKEN_PRICE


def calculate_cost(usage: Usage, model_ref: str, provider_id: str) -> float:
    """
    Calculate the estimated cost of a request.

    This function attempts to calculate the cost using the Pydantic genai_prices library. If it encounters any issues (e.g., missing model information, API errors), it falls back to a default pricing strategy based on token count and default values.

    Parameters
    ----------
    usage : Usage
        A genai_prices.Usage object containing the input and output token counts.
    model_ref : str
        A string reference to the model being used (e.g., "zai-org/GLM-4.5-Air-FP8").
    provider_id : str
        A string identifying the provider (e.g., "zai-org").

    Returns
    -------
    float
        A float representing the estimated cost of the request in USD.
    """
    try:
        cost = calc_price(
            usage=usage,
            model_ref=model_ref,
            provider_id=provider_id
        ).total_price
    except Exception as e:
        cost = (usage.input_tokens / 1_000_000) * DEFAULT_INPUT_MTOKEN_PRICE + (usage.output_tokens / 1_000_000) * DEFAULT_OUTPUT_MTOKEN_PRICE
        print(f"WARNING: Price calculation failed with error: {e}. Falling back to default pricing. Estimated cost: ${cost:.6f}")
    
    return float(cost)