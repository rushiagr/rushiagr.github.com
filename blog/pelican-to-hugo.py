import os

# NOTE: assumes 'Category: ' is the last values in heading of a pelican
# markdown

markdown_dir = '/home/r/src/blog/npf/content/blog/markdowns/'

files = os.listdir(markdown_dir)

for f in files:
    if f.endswith('.markdown'):
        with open(markdown_dir+f, 'r') as in_f:
            # files shouldn't have more than one dot
            outfile_name = f.split('.')[-2] + '.md'
            with open(markdown_dir+outfile_name, 'w') as out_f:
                out_f.write('+++\n')
                lines = in_f.readlines()
                for line in lines:
                    if line.startswith('Title: '):
                        _, title = line.split(':', 1)
                        title = title.strip()
                        out_f.write('title = "'+title+'"\n')
                    elif line.startswith('Date: '):
                        _, date = line.split(':', 1)
                        date = date.strip()
                        out_f.write('date = "'+date+'T00:00:00-00:00"\n')
                    elif line.startswith('Author: '):
                        continue
                    elif line.startswith('Summary: '):
                        continue
                    elif line.startswith('Slug: '):
                        continue
                    elif line.startswith('Tags: '):
                        _, tags = line.split(':', 1)
                        tags = tags.strip().split(',')
                        tags = ['"'+tag.strip()+'"' for tag in tags]
                        tags = ', '.join(tags)
                        out_f.write('tags = ['+tags+']\n')
                    elif line.startswith('Category: '):
                        out_f.write('type = "post"\n')
                        out_f.write('+++\n')
                        pass
                    else:
                        out_f.write(line)
