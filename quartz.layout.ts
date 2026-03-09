import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "О курсе": "/",
    },
  }),
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs({
        spacerSymbol: "›",
        rootName: "Главная",
        resolveFrontmatterTitle: true,
        showCurrentPage: true,
      }),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        { Component: Component.Search(), grow: true },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.DesktopOnly(
      Component.Explorer({
        title: "Курсы",
        folderClickBehavior: "link",
        folderDefaultState: "collapsed",
        useSavedState: true,
        sortFn: (a, b) => {
          if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
          return a.displayName.localeCompare(b.displayName, "ru", {
            numeric: true,
            sensitivity: "base",
          })
        },
        filterFn: (node) => {
          const hide = new Set(["tags"])
          return !hide.has(node.displayName.toLowerCase())
        },
      })
    ),
  ],
  right: [
    Component.Graph({
      localGraph: {
        drag: true,
        zoom: true,
        depth: 1,
        scale: 1.1,
        repelForce: 0.5,
        centerForce: 0.3,
        linkDistance: 30,
        fontSize: 0.6,
        opacityScale: 1,
        showTags: false,
        enableRadial: false,
      },
      globalGraph: {
        drag: true,
        zoom: true,
        depth: -1,
        scale: 0.9,
        repelForce: 0.5,
        centerForce: 0.3,
        linkDistance: 30,
        fontSize: 0.6,
        opacityScale: 1,
        showTags: false,
        enableRadial: true,
      },
    }),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks({ hideWhenEmpty: true }),
  ],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs({
      spacerSymbol: "›",
      rootName: "Главная",
      resolveFrontmatterTitle: true,
      showCurrentPage: true,
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        { Component: Component.Search(), grow: true },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.DesktopOnly(
      Component.Explorer({
        title: "Курсы",
        folderClickBehavior: "link",
        folderDefaultState: "collapsed",
        useSavedState: true,
        sortFn: (a, b) => {
          if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
          return a.displayName.localeCompare(b.displayName, "ru", {
            numeric: true,
            sensitivity: "base",
          })
        },
        filterFn: (node) => {
          const hide = new Set(["tags"])
          return !hide.has(node.displayName.toLowerCase())
        },
      })
    ),
  ],
  right: [],
}
