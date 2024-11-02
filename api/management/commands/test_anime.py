from django.core.management.base import BaseCommand
from api.models import Anime, IncompleteData, Poster, Genre,Studio, ExternalLink, Topic,Character, CharacterRole, Person, PersonRole, Related, Manga, Video, Screenshot, ScoresStat, StatusesStat
import json
from django.utils import timezone
import requests
import logging

logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://shikimori.one/api/graphql"
        payload = {
            "query": "{ animes(search: \"bakemono\", limit: 1, kind: \"movie\") { id name russian licenseNameRu english japanese synonyms kind rating score status episodes episodesAired duration airedOn { year month day date } releasedOn { year month day date } url season poster { id originalUrl mainUrl } fansubbers fandubbers licensors createdAt updatedAt nextEpisodeAt isCensored genres { id name russian kind } studios { id name imageUrl } externalLinks { id kind url createdAt updatedAt } personRoles { id rolesRu rolesEn person { id name poster { id } } } characterRoles { id rolesRu rolesEn character { id name poster { id } } } related { id anime { id name } manga { id name } relationKind relationText } videos { id url name kind playerUrl imageUrl } screenshots { id originalUrl x166Url x332Url } scoresStats { score count } statusesStats { status count } description descriptionHtml descriptionSource } }"
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
            'Host': 'shikimori.one',
        }

        response = requests.post(url, headers=headers, json={'query': payload['query']})
        if response.status_code == 200:
            data = response.json()

        if data['data']['animes'] is not None:
            data = response.json()
            animes = data.get('data').get('animes')
        else:
            raise ValueError('No animes found')
        for data in animes:
            if 'airedOn' in data:
                data["airedOn"] = IncompleteData.objects.create(
                    year=data['airedOn'].get('year') or False,
                    month=data['airedOn'].get('month') or None,
                    day=data['airedOn'].get('day') or None,
                )
            if 'releasedOn' in data:
                data["releasedOn"] = IncompleteData.objects.create(
                    year=data['releasedOn'].get('year') or False,
                    month=data['releasedOn'].get('month') or None,
                    day=data['releasedOn'].get('day') or None,
                )
            if 'poster' in data:
                data['poster'] , created = Poster.objects.update_or_create(
                    id=data['poster'].pop('id') or None,
                    defaults={
                        **data['poster']
                    }
                )

            append_data = {
                "studios": data.pop('studios', []) or [],
                "genres" : data.pop('genres', None) or [],
                "externalLinks" : data.pop('externalLinks', None) or [],
                'characterRoles' : data.pop('characterRoles', None) or [],
                'personRoles': data.pop('personRoles', None) or [],
                'related': data.pop('related', None) or [],
                'videos' : data.pop('videos', None) or [],
                'screenshots' : data.pop('screenshots', None) or [],
                'scoresStats' : data.pop('scoresStats', None) or [],
                'statusesStats' : data.pop('statusesStats', None) or [],
            }
            anime_instance, created = Anime.objects.update_or_create(
                id=data.pop('id', None),
                defaults={
                    **data
                }
            )

            def update_or_create_related_objects(model, data):
                return [
                    model.objects.update_or_create(
                        id=(int(item.pop('id', None)) if item.get('id') is not None else None),
                        defaults={**item}
                    )[0]  # Получаем первый элемент (экземпляр модели)
                    for item in data
                ]

            if append_data['studios']:
                studios_append = update_or_create_related_objects(Studio, append_data['studios'])
                anime_instance.studios.set(studios_append)

            if append_data['genres']:
                genres_append = update_or_create_related_objects(Genre, append_data['genres'])
                anime_instance.genres.set(genres_append)

            if append_data['externalLinks']:
                external_links = update_or_create_related_objects(ExternalLink, append_data['externalLinks'])
                anime_instance.externalLinks.set(external_links)
            if append_data['videos']:
                videos = update_or_create_related_objects(Video, append_data['videos'])
                anime_instance.videos.set(videos)
            if append_data['screenshots']:
                screenshots = update_or_create_related_objects(Screenshot, append_data['screenshots'])
                anime_instance.screenshots.set(screenshots)
            if append_data['scoresStats']:
                scorestats = update_or_create_related_objects(ScoresStat, append_data['scoresStats'])
                anime_instance.scoresStats.set(scorestats)
            if append_data['statusesStats']:
                statusesStats = update_or_create_related_objects(StatusesStat, append_data['statusesStats'])
                anime_instance.statusesStats.set(statusesStats)


            if append_data['characterRoles']:
                characterRoles_append = []
                for characterRole in append_data['characterRoles']:
                    character = characterRole.pop('character')

                    if character:
                        # Обработка постера
                        if (poster := character.pop('poster', None)):
                            poster_instance = update_or_create_related_objects(Poster, [poster])[0]
                            character['poster'] = poster_instance
                        character_instance = update_or_create_related_objects(Character, [character])[0]
                        characterRole['character'] = character_instance

                    characterRole_instance = update_or_create_related_objects(CharacterRole, [characterRole])[0]
                    characterRoles_append.append(characterRole_instance)
                anime_instance.characterRoles.set(characterRoles_append)

            if append_data['personRoles']:
                personRoles_append = []
                for personRole in append_data['personRoles']:
                    person = personRole.pop('person')
                    if person:
                        poster = person.pop('poster', None)
                        if poster:
                            person_instance = update_or_create_related_objects(Poster, [poster])[0]
                            person['poster'] = person_instance
                        person_instance = update_or_create_related_objects(Person, [person])[0]
                        personRole['person'] = person_instance
                    personRole_instance = update_or_create_related_objects(PersonRole, [personRole])[0]
                    personRoles_append.append(personRole_instance)
                anime_instance.personRoles.set(personRoles_append)

            if append_data['related']:
                related_append = []
                for related in append_data['related']:

                    if related_anime := related.pop('anime', None):
                        try:
                            related_anime_instance = Anime.objects.get(id=related_anime.pop('id'))
                        except Anime.DoesNotExist:
                            related_anime_instance = None
                        related_anime['anime'] = related_anime_instance
                    if related_manga := related.pop("manga", None):
                        related_manga_instance, create = Manga.objects.update_or_create(
                            id=(int(related_manga.pop('id', None)) if related_manga.get('id') is not None else None),
                            defaults={
                                **related_manga
                            }
                        )
                        related['manga'] = related_manga_instance
                    related_instance = update_or_create_related_objects(Related, [related])[0]
                    related_append.append(related_instance)
                anime_instance.related.set(related_append)
