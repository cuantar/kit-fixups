#!/usr/bin/env python3

from bs4 import BeautifulSoup
from packaging import version

async def generate(hub, **pkginfo):

	user = "kdave"
	pkg_name = pkginfo["name"]
	url = f"https://www.kernel.org/pub/linux/kernel/people/{user}/{pkg_name}/"
	html_data = await hub.pkgtools.fetch.get_page(url)
	vers = []
	soup = BeautifulSoup(html_data, "html.parser")
	for link in soup.find_all("a"):
		href = link.get("href")
		if href.endswith(".tar.xz"):
			vers.append( href.split(pkg_name)[1].split(".tar")[0].split("-")[-1])

	latest_version = sorted(vers, key=lambda v: version.parse(v)).pop()

	final_name = f"{pkg_name}-{latest_version}.tar.xz"
	url = f"{url}{final_name}"

	ebuild = hub.pkgtools.ebuild.BreezyBuild(
		**pkginfo,
		version=latest_version.lstrip("v"),
		artifacts=[hub.pkgtools.ebuild.Artifact(url=url, final_name=final_name)],
	)
	ebuild.push()

# vim: ts=4 sw=4 noet