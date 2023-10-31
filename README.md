# Puhul 🍈

This runs [xml2rfc](https://github.com/ietf-tools/xml2rfc/) on all RFCs with a `.xml` file to generate text RFC output.

New text RFC output is compared with the original and any differences are saved in the [text_results](text_results).

New HTML RFC output is compared with the original and any differences are saved in the [html_results](html_results).

In `html_results`, `*.diff.txt` files have plain diff of the HTML, `*.vdiff.html` files have visual diff from Selenium.

The `xml2rfc.txt` file inside result directories contains `xml2rfc` and other Python libraries' version information.
