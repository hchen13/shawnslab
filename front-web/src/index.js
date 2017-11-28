import React from 'react'
import ReactDOM from 'react-dom'

import 'antd/dist/antd.css'
import { Layout } from 'antd'

import './index.css'
import { Navbar, Hero, DataDisplay } from './components/components'

const { Content } = Layout

// ==========================================
class App extends React.Component {
	render() {
		return (
			<Layout className='main-layout'>
				<Navbar />

				<Content>
					<Hero />
					<DataDisplay />
				</Content>
			</Layout>
		)
	}
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
)