import CardProdutos from "./CardProdutos"

export default function CardList(props) {
    const { produtos } = props
    return (
        <div className="container">
            <div className="row g-3">
                {/* Estrutura de repetição map */}
                {produtos.map(function (produto, index) {
                    return (
                        <div className="col-12 col-sm-6 col-md-4 col-lg-3" key={index}>
                            <CardProdutos
                                nome={produto[1]}
                                descricao={produto[2]}
                                preco={produto[3]}
                                quantidade={produto[4]}
                            />
                        </div>
                    )
                })}

            </div>
        </div>

    )
}