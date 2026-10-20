import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_core.tools import tool


@tool
def calculate_discount(price : float , discount : float) -> float:
    """
    Calculate the final price after applying a discount
    Args:
        price : Original price of the product
        discount : Discount percentage    
    """

    return price - (price * discount/100)

def main() -> None:

    """
    Demonstrate creating a LangChain tool using decorator
    """

    print(f"Tool name : {calculate_discount.name}")
    print(f"Tool description : {calculate_discount.description}")
    print(f"Tool Input Schema : {calculate_discount.args_schema.model_json_schema()}")

    price = 1000.0
    discount = 20.0

    print(f"Price = {price} , Discount : {discount}")
    final_price = calculate_discount.invoke(
        {
            "price" : price,
            "discount" : discount
        }
    )
    print(final_price)


if __name__ == "__main__":
    main()