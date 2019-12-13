import glob, os, re, numpy as np, pandas as pd
from slugify import slugify
from PIL import Image

class WSBCatalog():

    def __init__(self, file='data/wsb-catalog.csv'):
        self._citation_schemes = { 'schottlaender/4.0/': 'Schottlaender ', 'maynard-and-miles/': 'Maynard & Miles ', 'shoaf/': 'Shoaf ' }
        self._items = pd.read_csv(file)
        self._items = self._items.fillna('')
        self._add_missing_identifiers()
        self._add_missing_thumbnails()
        self._sort()
        self._generate_markdown()

    def get_items(self):
        return self._items

    def put_items(self, item):
        self._items = items

    # write catalog data to file
    def to_csv(self, file='data/wsb-catalog.csv'):
        items = self._items[['identifier', 'creator', 'title', 'publisher', 'date', 'bibliographicCitation', 'description']]
        items.to_csv(file, index=False)

    # write catalog Markdown to file
    def to_markdown(self, file='docs/index.md'):
        # write index.md
        with open(file, 'w') as outfile:
            for line in self._index_markdown():
                outfile.write(line + '\n')
        # for each item write its item page
        for index, item in self._items.iterrows():
            with open('docs/{}.md'.format(item['itemPage']), 'w') as outfile:
                outfile.write(item['mdItemPage'])

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
                while new_id in ids or new_id in new_ids:
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
        for infile in glob.glob("docs/assets/images/*.jpg"):
            outfile = "docs/assets/thumbnails/" + os.path.split(infile)[1]
            if not glob.glob(outfile):
                try:
                    im = Image.open(infile)
                    im.thumbnail(size)
                    im.save(outfile, "JPEG")
                    print('Added new thumbnail:', outfile)
                except IOError:
                    print("Cannot create thumbnail for", infile)

    # Sort items by dc:date and dc:bibliographicCitation
    def _sort(self):
        self._items['primaryCitePadded'] = self._items["bibliographicCitation"].astype('str').apply(lambda x: self._pad_primary_cite_code(x))
        self._items = self._items.sort_values(by=['date', 'primaryCitePadded'])
        self._items = self._items[['identifier', 'creator', 'title', 'publisher', 'date', 'bibliographicCitation', 'description']]

    # Generate Markdown from dataframe
    def _generate_markdown(self):
        items = pd.DataFrame(self._items, copy=True)
        items['image'] = items['identifier'].astype('str').apply(lambda x: 'assets/images/{}.jpg'.format(x))
        items['thumbnail'] = items['identifier'].astype('str').apply(lambda x: 'assets/thumbnails/{}.jpg'.format(x))
        items['itemPage'] = items['identifier'].astype('str').apply(lambda x: 'pages/{}'.format(x))
        items = items.fillna('')
        items['prettyBibliographicCitation'] = items['bibliographicCitation'].astype('str').apply(lambda x: self._format_bibliographicCitation(x))
        items['entry'] = np.where(items['publisher'] == '', 'n.p.', items['publisher'])
        items['entry'] = items.apply(lambda x: '{}, {}. {} {}'.format(x['entry'], x['date'], x['description'], x['prettyBibliographicCitation']), axis=1)
        items['mdTableRow'] = items.apply(lambda x: '|[![{}]({})]({}.html)|{}|{}|{}|'.format(x['title'], x['thumbnail'], x['itemPage'], x['creator'], x['title'], x['entry']), axis=1)
        items['mdItemPage'] = items.apply(lambda x: '## {}. {}.\n\n{}\n\n![{}](../{})\n'.format(x['creator'], x['title'], x['entry'], x['title'], x['image']), axis=1)
        self._items = items

    def _index_markdown(self):
        table_header = ['|image|creator|title|description|', '|---|---|---|---|']
        table_body = pd.Series(self._items['mdTableRow']).tolist()
        table = table_header + table_body
        return table

    def _item_page_markdown(self):
        return pd.Series(self._items['mdItemPage']).tolist()

if __name__ == "__main__":
    print('Building catalog...')
    catalog = WSBCatalog()
    catalog.to_markdown()
    print('Done.')
