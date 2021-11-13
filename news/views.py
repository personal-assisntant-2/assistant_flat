from django.shortcuts import render
from .settings import handlers
import asyncio


async def new_view(request):
    """
    Requests the actual information from the resources specified in "handlers", if the response status is 200 - parses
    it and returns it, otherwise - "".
    """
    # formation of a list of tasks
    list_handlers = [handler for key, handler in handlers.items()]

    # run the tasks and get the result,
    # for example - [{'bitcoin': '66,652.70', 'ethereum': '4,706.51', 'bitcoin_cash': ''}, ...]
    list_context = await asyncio.gather(*[func() for func in list_handlers], return_exceptions=True)

    # forms a context in the form:
    # {'rates_bitstat': {'bitcoin': '66,652.70', 'ethereum': '4,706.51', 'bitcoin_cash': ''}, ...}
    context = dict()
    for index, key in enumerate(handlers):
        context[key] = list_context[index]

    return render(request, 'news/news.html', context)



