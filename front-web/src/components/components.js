import React from 'react'
import { Layout, Row, Col, Calendar, Menu, Icon, Button } from 'antd'
import './components.css'

const { Header } = Layout

export class Logo extends React.Component {
	render() {
		return (
			<div className='logo'>小明实验室</div>
		)
	}
}

export class Navbar extends Header {
	render() {
		return (
			<Header>
				<Row type='flex' align='middle'>
					<Col span={6}><Logo /></Col>
				</Row>
			</Header>
		)
	}
}

export class Hero extends React.Component {
	render() {
		return (
			<Row type='flex'>
				<Col span={24}>
					<div className='hero'>
						<Row>
							<Col span={6}>
								<label>最新净值</label>
								<div className='hero-text lg'>1.1845</div>
							</Col>
							<Col span={6}>
								<label>总数据量</label>
								<div className='hero-text md'>182</div>
								<label>平均净值</label>
								<div className='hero-text md'>1.0456</div>
							</Col>
							<Col span={6}>
								<label>历史最高</label>
								<div className='hero-text md'>1.20</div>
								<label>历史最低</label>
								<div className='hero-text md'>0.9123</div>
							</Col>
							<Col span={6}>
								<label>更新时间</label>
								<div className='hero-text md'>15:35</div>
								<label>跟踪状态</label>
								<div className='hero-text md'>在线</div>
							</Col>
						</Row>
					</div>
				</Col>
			</Row>
		)
	}
}

export class DataDisplay extends React.Component {
	constructor(props) {
		super(props)
		this.getNetValue = this.getNetValue.bind(this)
		this.dateCellRender = this.dateCellRender.bind(this)
	}

	getNetValue(moment) {
		let year 	= moment.year(),
				month	= moment.month(),
				date 	= moment.date()

		return (Math.random() + 1).toFixed(2)
	}

	dateCellRender(moment) {
		var netValue = this.getNetValue(moment)
		return (
			<div className='net-value'>{netValue}</div>
		)
	}

	render() {
		return (
			<Row style={{ background: "#fff", padding: '16px'}}>
				<Col span={15}>
					<Calendar dateCellRender={this.dateCellRender} fullscreen={false} className='calendar-view' />
				</Col>
				<Col span={9} style={{ paddingLeft: '50px' }}>
					<Button type='primary' icon='download' size='large'>下载数据</Button>
				</Col>
			</Row>
		)
	}
}