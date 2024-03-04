import re


def replace_pre_with_div_in_quarto_html(mdx_content):
    # Function to replace <pre> tags with <div> tags in each HTML string
    def replace_pre_with_div(html_str):
        # Replace opening <pre> tag with <div>
        new_str = re.sub(r"^<pre(.*?)>", r"<div\1>", html_str)
        # Replace closing </pre> tag with </div>
        new_str = re.sub(r"</pre>$", "</div>", new_str)
        return new_str

    # Regex to find the quartoRawHtml variable definition and its content
    quarto_raw_html_pattern = r"quartoRawHtml\s*=\s*\[((?:.|\n)*?)\];"

    # Find the quartoRawHtml variable content
    match = re.search(quarto_raw_html_pattern, mdx_content)

    if match:
        # Extract the content within the brackets
        quarto_raw_html_content = match.group(1)

        # Split the content into individual HTML strings, considering `,` outside of the backticks
        html_strings = re.findall(r"`((?:.|\n)*?)`", quarto_raw_html_content)

        # Replace <pre> with <div> for each HTML string
        edited_html_strings = [replace_pre_with_div(html) for html in html_strings]

        # Reconstruct the quartoRawHtml variable content
        edited_quarto_raw_html_content = ",\n".join(
            [f"`{html}`" for html in edited_html_strings]
        )

        # Replace the original content in mdx_content
        edited_mdx_content = re.sub(
            quarto_raw_html_pattern,
            f"quartoRawHtml = [\n{edited_quarto_raw_html_content}\n];",
            mdx_content,
        )

        return edited_mdx_content
    else:
        return mdx_content


if __name__ == "__main__":
    # Find all mdx files in the repo
    import glob
    import os

    mdx_files = []
    for root, dirs, files in os.walk(os.path.dirname(os.path.dirname(__file__))):
        for file in glob.glob(os.path.join(root, "*.mdx")):
            with open(file, "r") as f:
                mdx_content = f.read()
                edited_mdx_content = replace_pre_with_div_in_quarto_html(mdx_content)
                if edited_mdx_content != mdx_content:
                    with open(file, "w") as f:
                        f.write(edited_mdx_content)
                    mdx_files.append(file)

    print(f"replacements made in the following files: {mdx_files}")
