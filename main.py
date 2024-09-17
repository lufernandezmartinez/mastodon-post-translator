from mastodon import Mastodon

mastodon = Mastodon(
    access_token='',
    api_base_url='https://mastodon.social'
)

mastodon.status_post('Test!')