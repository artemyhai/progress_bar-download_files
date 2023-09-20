import asyncio
import httpx
import tqdm


# the name under which we save the downloaded files for visual distinction
async def download_files(url: str, filename: str):
    with open(filename, 'wb') as f:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as r:
                
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))

                tqdm_params = {
                    'desc': url,
                    'total': total,
                    'miniters': 1,
                    'unit': 'it',
                    'unit_scale': True,
                    'unit_divisor': 1024,
                }

                with tqdm.tqdm(**tqdm_params) as pb:
                    async for chunk in r.aiter_bytes():
                        pb.update(len(chunk))
                        f.write(chunk)


async def main():

    '''Using the get_running_loop method and creating an asyncio module object which
     returns the running event loop on the current operating system thread.
     Next, using the create_task method, we create tasks for downloading files and running
     according to the list of addresses.
     Next, we call the gather method in asyncio, the method allows you to launch objects after the group
     competitive racing'''

    loop = asyncio.get_running_loop()

    urls = [
        ('https://files.icyflamestudio.com/10MB.bin', '10MB.bin'),
        ('https://files.icyflamestudio.com/20MB.bin', '20MB.bin'),
        ('https://files.icyflamestudio.com/50MB.bin', '50MB.bin'),
    ]

    tasks = [loop.create_task(download_files(url, filename)) for url, filename in urls]
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
    
