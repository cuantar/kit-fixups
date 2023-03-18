#!/usr/bin/env python3

from packaging import version


async def generate(hub, **pkginfo):
	github_user = "kubernetes-sigs"
	github_repo = pkginfo.get("name")

	release_data = await hub.pkgtools.fetch.get_page(
		f"https://api.github.com/repos/{github_user}/{github_repo}/releases",
		is_json=True,
	)

	try:
		latest_release = max(
			(
				release
				for release in release_data
				if not release["prerelease"] and not release["draft"]
			),
			key=lambda release: version.parse(release["tag_name"]),
		)
	except ValueError:
		raise hub.pkgtools.ebuild.BreezyError(
			f"Can't find suitable release of {github_repo}"
		)

	pkginfo['version'] = latest_version = latest_release["tag_name"].lstrip("v")

	source_url = latest_release["tarball_url"]
	source_name = f"{github_repo}-{latest_version}.tar.gz"

	pkginfo['artifacts'] = { 'main' : hub.pkgtools.ebuild.Artifact(url=source_url, final_name=source_name) }

	await hub.pkgtools.golang.add_gosum_bundle(hub, pkginfo)

	ebuild = hub.pkgtools.ebuild.BreezyBuild(
		**pkginfo,
		github_user=github_user,
		github_repo=github_repo
	)
	ebuild.push()
