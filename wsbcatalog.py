import glob, os, re, numpy as np, pandas as pd
from slugify import slugify
from PIL import Image

class WSBCatalog():

    def __init__(self, file='data/wsb-catalog.csv'):
        self._citation_schemes = { 'schottlaender/4.0/': 'Schottlaender ', 'maynard-and-miles/': 'Maynard & Miles ', 'shoaf/': 'Shoaf ' }
        self._items = pd.read_csv('data/wsb-catalog.csv')
        self._items = self._items.fillna('')
        self._add_missing_identifiers()
        self._add_missing_thumbnails()
        self._sort()

    def get_items(self):
        return self._items

    def put_items(self, item):
        self._items = items

    # write catalog data to file
    def to_csv(self, file='data/wsb-catalog.csv'):
        self._items.to_csv(file, index=False)

    # write catalog Markdown
    def to_markdown(self, file='docs/index.md'):
        with open(file, 'w') as outfile:
            for line in self._markdown_table():
                outfile.write(line + '\n')

    # write both data and Markdoen
    def build(self, csv_file='data/wsb-catalog.csv', md_file='docs/index.md'):
        self.to_csv(csv_file)
        self.to_markdown(md_file)

    def _pad_primary_cite_code(self, cite):
        primary_code = cite.split(', ')[0]
        p = re.compile('^(.*[A-Z])(\d+)(.*)$')
        m = p.match(primary_code)
        if m is not None:
            g = m.group(1,2,3)
            padded_code ='{}{:04d}{}'.format(g[0], int(g[1]), g[2])
            return padded_code
        else:
            return ''

    def _format_bibliographicCitation(self, cite):
        formatted_cite = []
        for prefix in self._citation_schemes:
            scheme = self._citation_schemes
            p = re.compile(prefix + '([A-Z]\d+\w*)')
            numbers = p.findall(cite)
            if numbers:
                if len(numbers) > 2:
                    formatted_cite.append(scheme[prefix] + ', '.join(numbers[:-1]) + ', and {}'.format(numbers[-1]))
                elif len(numbers) == 2:
                    formatted_cite.append(scheme[prefix] + ' and '.join(numbers))
                else:
                    formatted_cite.append(scheme[prefix] + numbers[0])
        if not formatted_cite:
            return ''
        else:
            return ', '.join(formatted_cite) + '.'

    # Add missing identifiers
    def _add_missing_identifiers(self):
        ids = self._items['identifier'].tolist()
        titles = self._items['title'].tolist()
        new_ids = []
        for idx, id in enumerate(ids):
            if id == '':
                i = 1
                slug = slugify('{:.30}'.format(titles[idx]))
                new_id = '{}-{:d}'.format(slug, i)
                while new_id in ids:
                    i += 1
                    new_id = '{}-{:d}'.format(slug, i)
                new_ids.append(new_id)
                print('Added new identifier:', new_id)
            else:
                new_ids.append(id)
        self._items["identifier"] = pd.Series(new_ids).values

    # Generate thumbnails from images
    def _add_missing_thumbnails(self):
        size = (300, 300)
        for infile in glob.glob("images/*.jpg"):
            outfile = "docs/thumbnails/" + os.path.split(infile)[1]
            try:
                im = Image.open(infile)
                im.thumbnail(size)
                im.save(outfile, "JPEG")
            except IOError:
                print("cannot create thumbnail for", infile)

    # Sort items by dc:date and dc:bibliographicCitation
    def _sort(self):
        self._items['primaryCitePadded'] = self._items["bibliographicCitation"].astype('str').apply(lambda x: self._pad_primary_cite_code(x))
        self._items = self._items.sort_values(by=['date', 'primaryCitePadded'])
        self._items = self._items[['identifier', 'creator', 'title', 'publisher', 'date', 'bibliographicCitation', 'description']]

    # Generate Markdown from dataframe
    def _markdown_table(self):
        items = pd.DataFrame(self._items, copy=True)
        items['image'] = items['identifier'].astype('str').apply(lambda x: 'thumbnails/{}.jpg'.format(x))
        items = items.fillna('')
        items['bibliographicCitation'] = items['bibliographicCitation'].astype('str').apply(lambda x: self._format_bibliographicCitation(x))
        items['entry'] = np.where(items['publisher'] == '', 'n.p.', items['publisher'])
        items['entry'] = items.apply(lambda x: '{}, {}. {} {}'.format(x['entry'], x['date'], x['description'], x['bibliographicCitation']), axis=1)
        items['mdTableRow'] = items.apply(lambda x: '|![{}]({})|{}|{}|{}|'.format(x['identifier'], x['image'], x['creator'], x['title'], x['entry']), axis=1)
        table_header = ['|image|creator|title|description|', '|---|---|---|---|']
        table_body = pd.Series(items['mdTableRow']).tolist()
        table = table_header + table_body
        return table

if __name__ == "__main__":
    print('Building catalog...')
    catalog = WSBCatalog()
    catalog.build()
    print('Done.')
