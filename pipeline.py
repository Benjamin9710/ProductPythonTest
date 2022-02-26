import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    """The implementation of the pipeline test."""

    product_list = []  # store list of all product tuples

    for product in product_data:

        display_product = True  # store variable that determines whether to display the product

        p_name = product["name"]  # store current product name
        p_tags = product["tags"]  # store current product tags
        p_code = product["code"]  # store current product code

        # Determines whether to display or hide items if an include_tags list is specified
        if include_tags:

            display_check_all_tags = False  # store of whether to display variable after all tags have been checked
                                            # in include_tags functionality
            for include_tag in include_tags:

                for p_tag in p_tags:
                    if include_tag == p_tag:
                        display_check_all_tags = True

            if not display_check_all_tags:
                display_product = False

        # Determines whether to display or hide items if an exclude_tags list is specified
        if exclude_tags:
            for exclude_tag in exclude_tags:
                for p_tag in p_tags:
                    if exclude_tag == p_tag:
                        display_product = False

        product_count = 0  # store of current product interation in iteration loop
        # If the product is to be displayed, determines whether the product has already been stored as a tuple in the
        # list. If it has not been stored in the list, a new tuple is created an appended into the product_list
        # variable, otherwise if it has already been stored, the product_code is appended to the correct tuple
        if display_product:

            product_stored = False
            for product_list_item in product_list:
                if product_list_item.product_name == p_name:
                    product_list[product_count].product_codes.append(p_code)
                    product_stored = True

                product_count += 1

            if not product_stored:
                product_tuple = PreferenceMatch(p_name, [p_code])
                product_list.append(product_tuple)

    return product_list

    pass


if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]


    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))
