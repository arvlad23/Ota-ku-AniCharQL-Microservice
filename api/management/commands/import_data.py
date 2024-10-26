import requests
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import data'

    def handle(self, *args, **options):
        # Убедитесь, что URL правильный
        url = 'https://shikimori.one/api/graphql'  # или 'https://shikimori.one/graphql'

        # Заголовки для запроса
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
            'Accept': '*/*',
            'Content-Type': 'application/json',
        }

        # Ваш payload (запрос GraphQL)
        payload = {
            "query": """
            {
              animes(search: "bakemono", limit: 1, kind: "!special") {
                id
                malId
                name
                russian
                licenseNameRu
                english
                japanese
                synonyms
                kind
                rating
                score
                status
                episodes
                episodesAired
                duration
                airedOn {
                  year
                  month
                  day
                  date
                }
                releasedOn {
                  year
                  month
                  day
                  date
                }
                url
                season
                poster {
                  id
                  originalUrl
                  mainUrl
                }
                fansubbers
                fandubbers
                licensors
                createdAt
                updatedAt
                nextEpisodeAt
                isCensored
                genres { id name russian kind }
                studios { id name imageUrl }
                externalLinks {
                  id
                  kind
                  url
                  createdAt
                  updatedAt
                }
                personRoles {
                  id
                  rolesRu
                  rolesEn
                  person { id name poster { id } }
                }
                characterRoles {
                  id
                  rolesRu
                  rolesEn
                  character { id name poster { id } }
                }
                related {
                  id
                  anime {
                    id
                    name
                  }
                  manga {
                    id
                    name
                  }
                  relationKind
                  relationText
                }
                videos { id url name kind playerUrl imageUrl }
                screenshots { id originalUrl x166Url x332Url }
                scoresStats { score count }
                statusesStats { status count }
                description
                descriptionHtml
                descriptionSource
              }
            }
            """,
        }

        # Отправка запроса
        response = requests.post(url, headers=headers, json=payload)

        # Печать ответа
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
