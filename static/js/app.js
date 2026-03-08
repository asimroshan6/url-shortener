async function shortenUrl(){
    const shorten_input = document.getElementById("urlInput").value;
    const url_area = document.getElementById("shortUrl");


    try{
        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({url: shorten_input})
        }
        );
        const data = await response.json();
        console.log(data);
        if (response.status === 429) {
            const retryAfter = response.headers.get('Retry-After') || 'a few';
            url_area.value = `rate limit exceeded, do after ${retryAfter} seconds`
            return;
        } else if (!response.ok){
            url_area.value = data.detail[0].msg || "Some error occurred";
            return;
        }
        url_area.value = data.short_url;
        
    } catch (e){
        console.log("error " + e);
    }
}

async function copyUrl() {
  const shortUrlInput = document.getElementById("shortUrl");
  try {
    await navigator.clipboard.writeText(shortUrlInput.value);
    alert("Short URL copied!");
  } catch (err) {
    console.error("Failed to copy: ", err);
  }
}
