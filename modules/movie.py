import aiohttp

from lib.cog import Cog
from lib.command import Command, makeCommand


class Movie(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.apikey = self.settings["api_key"]
        self.search_url = "https://api.themoviedb.org/3/search/multi?api_key={}&query={}"
        # self.movie_url = ""
        # self.tv_url = ""
        self.id_url = "https://api.themoviedb.org/3/{media_type}/{id}?api_key="

    @makeCommand(aliases=["imdb"],
                 description="<query> search The Movie Db for TV and movies")
    async def search(self, c: Command):
        query = c.message
        # TODO handle years in query
        response = await self.apiget(self.search_url.format(
            self.apikey, query))
        print(response)
        if response is None or "results" not in response:
            await self.send_message("Couldn't find that m8")
        elif len(response["results"]) == 0:
            await self.send_message("Couldn't find that m8")
        else:
            info = await self.apiget(
                self.id_url.format(**response["results"][0]) + self.apikey)
            if response["results"][0]["media_type"] == "movie":
                await self.send_message(
                    self.formatresponse(info, is_movie=True))
                await self.send_message(response["results"][0]["overview"])
            else:
                await self.send_message(
                    self.formatresponse(info, is_movie=False))

    # TODO
    @makeCommand(aliases=["movie"],
                 description="<query> search The Movie Db for Movies")
    async def movie_search(self, query):
        pass

    # TODO
    @makeCommand(aliases=["tv"],
                 description="<query> search The Movie Db for TV shows")
    async def tv_search(self, query):
        pass

    async def apiget(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    def formatresponse(self, info: dict, is_movie: bool):
        # gross
        if is_movie:
            response = """:popcorn: *{original_title}* ({release_date}) _{vote_average}_ —https://imdb.com/title/{imdb_id}""".format(
                **info)
        else:
            response = """
            {original_name} ({first_air_date}\n
            Rating: {vote_average})\n
            Episodes: {episode_run_time[0]}\n
            —{overview}
            """.format(**info)
        return response
