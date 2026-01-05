import pathlib
import json
from py.model.Comment import Comment
from py.model.Post import Post
from py.model.Author import Author
from py.model.EmbeddedSentence import EmbeddedSentence
# testing serialization
root = r'C:\Users\wslam\Everything\health_city_lab\project1\hcl-project\src'
cwd = pathlib.Path(root)

scraped_path = cwd / 'data' / 'Scrape_Output' / 'ALZConnected' / 'test_serialization.jsonl'
embed_path = cwd / 'data' / 'Embed_Output' / 'ALZConnected' / 'test_serialization.jsonl'

def get_comment_test() -> Comment:
    url = 'https:test'
    post_id = '123'
    author = Author('user_name_test', 'user_id_test', 'user_link_test')
    content = ['test content']
    date = 'test_date'
    comment = Comment(url, post_id, date, author, content)
    return comment

def get_post_test() -> Post:
    url = 'https:test'
    post_id = '123'
    title = 'title_test'
    author = Author('user_name_test', 'user_id_test', 'user_link_test')
    content = ['test content']
    date = 'test_date'
    comments = [get_comment_test() for i in range(5)]
    post = Post(
        url=url,
        post_id=post_id,
        title=title,
        content=content,
        date=date,
        author=author,
        comments=comments
    )

    return post

def save_post(post: Post) -> None:
    with open(scraped_path, 'w') as f:
        f.write(json.dumps(post.to_dict()))

def load_post() -> Post:
    with open(scraped_path, 'r') as f:
        line = f.readline()
        post = Post.from_dict(json.loads(line))
        return post

def test_post_identity(A: Post, B: Post) -> bool:
    assert A == B, 'POSTS NOT EQUAL'
    return A == B

def test_scrape_serialization() -> None:
    post = get_post_test()
    save_post(post)
    loaded = load_post()
    assert test_post_identity(post, loaded), 'post serialization failed'
    if test_post_identity(post, loaded):
        print('serialization success')




