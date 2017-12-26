# Distributed under the terms of the GNU General Public License v2

EAPI=6
GNOME2_LA_PUNT="yes"

inherit gnome2

DESCRIPTION="Evolution module for connecting to Microsoft Exchange Web Services"
HOMEPAGE="https://wiki.gnome.org/Apps/Evolution"

LICENSE="LGPL-2.1"
SLOT="0"
KEYWORDS="~*"
IUSE="test"

RDEPEND="
	dev-db/sqlite:3=
	>=dev-libs/glib-2.40:2
	dev-libs/libical:0=
	>=dev-libs/libxml2-2
	>=gnome-extra/evolution-data-server-3.20.5
	>=mail-client/evolution-3.20.5
	>=net-libs/libsoup-2.42:2.4
	>=x11-libs/gtk+-3:3
"
DEPEND="${RDEPEND}
	>=dev-util/gtk-doc-am-1.9
	>=dev-util/intltool-0.35.5
	virtual/pkgconfig
	test? ( net-libs/uhttpmock )
"

src_configure() {
	# We don't have libmspack, needing internal lzx
	gnome2_src_configure \
		--with-internal-lzx \
		$(use_enable test tests)
}
