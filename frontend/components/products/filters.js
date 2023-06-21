const filters = [
    { name: "Название", key: "name" },
    { name: "Популярность", key: "popularity" },
    { name: "Цена", key: "price" },
]

const default_filter = filters[2]
const default_order = "desc"

export { filters, default_filter, default_order }
