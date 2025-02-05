def add_pdf_highlighting(page_index, page, bbox, doc):
    # Highlight the bbox
    highlight = page.add_rect_annot(bbox)
    highlight.set_colors({"stroke": (1, 0, 0), "fill": (1, 1, 0)})  # Red stroke, yellow fill
    highlight.update()

    # Save the modified PDF without incremental saving
    output_path = "highlighted_output" + str(page_index) + ".pdf"
    doc.save(output_path)
    print(f"Highlighted PDF saved to {output_path}")

def standardise_country_names(df):
    country_dictionary = {
        "Türkiye": "Turkey",
        "Cyprus (South)": "Cyprus",
        """Republic of                     +
        | Ireland""": "Ireland",
        "United States": "USA",
        "Scotland": "United Kingdom"
    }
    df['country'] = df['country'].apply(lambda x: country_dictionary.get(x, x))
    return df
