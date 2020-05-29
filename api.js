addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
    const l = [
        "timelt",
        "timegt",
        "address_type",
        "arch",
        "asn",
        "city",
        "country",
        "name",
        "pkgrel",
        "pkgver",
        "protocol",
        "region",
        "source",
        "ua"
    ]
    let exit = false
    let sql = 'select count("value") from pkgstats where 1=1 '
    const url = new URL(request.url)
    if (url.search === "") {
        return new Response(JSON.stringify(l), {
            status: 200
        })
    }
    const queryString = url.search.slice(1).split('&')
    queryString.forEach(item => {
        const kv = item.split('=')
        if (kv[0] && kv[1]) {
            if (l.indexOf(kv[0]) === -1) {
                exit = true
                return
            }
            if (kv[0] === "timelt") {
                sql += `and time < ${kv[1] * 1000000000} `
                return
            }
            if (kv[0] === "timegt") {
                sql += `and time > ${kv[1] * 1000000000} `
                return
            }
            sql += `and "${kv[0]}" = '${kv[1]}' `
        }
    })
    if (exit) {
        return new Response(JSON.stringify(l), {
            status: 200
        })
    }
    const formData = new FormData();
    formData.append("q", sql)
    const resp = await fetch('https://influxdb.example.com/query?db=archcn&u=archcnro&p=password', {
        method: 'POST',
        body: formData
    })
    const json = await resp.json()
    if (json['results'][0]['series'] === undefined) {
        return new Response(JSON.stringify({
            'sql': sql,
            'count': 0
        }), {
            status: 200
        })
    }
    return new Response(JSON.stringify({
        'sql': sql,
        'count': json['results'][0]['series'][0]['values'][0][1]
    }), {
        status: 200
    })
}
