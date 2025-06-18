#!/bin/bash

# MatchedCover Insurance Hyperledger Fabric Network Setup Script
# This script sets up a complete test network for blockchain-integrated insurance operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up MatchedCover Insurance Hyperledger Fabric Network${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}Creating network directories...${NC}"
mkdir -p fabric-config/{crypto-config,channel-artifacts,scripts,chaincode}
mkdir -p fabric-config/crypto-config/{ordererOrganizations,peerOrganizations}

# Generate crypto materials
echo -e "${YELLOW}Generating cryptographic materials...${NC}"

# Create crypto-config.yaml
cat > fabric-config/crypto-config.yaml << EOF
OrdererOrgs:
  - Name: Orderer
    Domain: matchedcover.com
    Specs:
      - Hostname: orderer
        SANS:
          - localhost
          - 127.0.0.1
          - orderer.matchedcover.com

PeerOrgs:
  - Name: Insurance
    Domain: insurance.matchedcover.com
    EnableNodeOUs: true
    Template:
      Count: 1
      SANS:
        - localhost
        - 127.0.0.1
        - "{{.Hostname}}.insurance.matchedcover.com"
    Users:
      Count: 1

  - Name: Reinsurance
    Domain: reinsurance.matchedcover.com
    EnableNodeOUs: true
    Template:
      Count: 1
      SANS:
        - localhost
        - 127.0.0.1
        - "{{.Hostname}}.reinsurance.matchedcover.com"
    Users:
      Count: 1
EOF

# Create configtx.yaml
echo -e "${YELLOW}Creating channel configuration...${NC}"
cat > fabric-config/configtx.yaml << EOF
Organizations:
  - &OrdererOrg
      Name: OrdererOrg
      ID: OrdererMSP
      MSPDir: crypto-config/ordererOrganizations/matchedcover.com/msp
      Policies:
        Readers:
          Type: Signature
          Rule: "OR('OrdererMSP.member')"
        Writers:
          Type: Signature
          Rule: "OR('OrdererMSP.member')"
        Admins:
          Type: Signature
          Rule: "OR('OrdererMSP.admin')"
      OrdererEndpoints:
        - orderer.matchedcover.com:7050

  - &Insurance
      Name: InsuranceMSP
      ID: InsuranceMSP
      MSPDir: crypto-config/peerOrganizations/insurance.matchedcover.com/msp
      Policies:
        Readers:
          Type: Signature
          Rule: "OR('InsuranceMSP.admin', 'InsuranceMSP.peer', 'InsuranceMSP.client')"
        Writers:
          Type: Signature
          Rule: "OR('InsuranceMSP.admin', 'InsuranceMSP.client')"
        Admins:
          Type: Signature
          Rule: "OR('InsuranceMSP.admin')"
        Endorsement:
          Type: Signature
          Rule: "OR('InsuranceMSP.peer')"
      AnchorPeers:
        - Host: peer0.insurance.matchedcover.com
          Port: 7051

  - &Reinsurance
      Name: ReinsuranceMSP
      ID: ReinsuranceMSP
      MSPDir: crypto-config/peerOrganizations/reinsurance.matchedcover.com/msp
      Policies:
        Readers:
          Type: Signature
          Rule: "OR('ReinsuranceMSP.admin', 'ReinsuranceMSP.peer', 'ReinsuranceMSP.client')"
        Writers:
          Type: Signature
          Rule: "OR('ReinsuranceMSP.admin', 'ReinsuranceMSP.client')"
        Admins:
          Type: Signature
          Rule: "OR('ReinsuranceMSP.admin')"
        Endorsement:
          Type: Signature
          Rule: "OR('ReinsuranceMSP.peer')"
      AnchorPeers:
        - Host: peer0.reinsurance.matchedcover.com
          Port: 9051

Capabilities:
  Channel: &ChannelCapabilities
    V2_0: true
  Orderer: &OrdererCapabilities
    V2_0: true
  Application: &ApplicationCapabilities
    V2_0: true

Application: &ApplicationDefaults
  Organizations:
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
    LifecycleEndorsement:
      Type: ImplicitMeta
      Rule: "MAJORITY Endorsement"
    Endorsement:
      Type: ImplicitMeta
      Rule: "MAJORITY Endorsement"
  Capabilities:
    <<: *ApplicationCapabilities

Orderer: &OrdererDefaults
  OrdererType: etcdraft
  EtcdRaft:
    Consenters:
    - Host: orderer.matchedcover.com
      Port: 7050
      ClientTLSCert: crypto-config/ordererOrganizations/matchedcover.com/orderers/orderer.matchedcover.com/tls/server.crt
      ServerTLSCert: crypto-config/ordererOrganizations/matchedcover.com/orderers/orderer.matchedcover.com/tls/server.crt
  Addresses:
    - orderer.matchedcover.com:7050
  BatchTimeout: 2s
  BatchSize:
    MaxMessageCount: 10
    AbsoluteMaxBytes: 99 MB
    PreferredMaxBytes: 512 KB
  Organizations:
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
    BlockValidation:
      Type: ImplicitMeta
      Rule: "ANY Writers"

Channel: &ChannelDefaults
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
  Capabilities:
    <<: *ChannelCapabilities

Profiles:
  TwoOrgsApplicationGenesis:
    <<: *ChannelDefaults
    Orderer:
      <<: *OrdererDefaults
      Organizations:
        - *OrdererOrg
      Capabilities: *OrdererCapabilities
    Application:
      <<: *ApplicationDefaults
      Organizations:
        - *Insurance
        - *Reinsurance
      Capabilities: *ApplicationCapabilities
EOF

# Generate crypto materials using cryptogen
echo -e "${YELLOW}Generating certificates and keys...${NC}"
if command -v cryptogen &> /dev/null; then
    cd fabric-config
    cryptogen generate --config=crypto-config.yaml
    cd ..
else
    echo -e "${RED}Warning: cryptogen not found. Using mock certificates for development.${NC}"
    # Create mock directory structure for development
    mkdir -p fabric-config/crypto-config/ordererOrganizations/matchedcover.com/orderers/orderer.matchedcover.com/{msp,tls}
    mkdir -p fabric-config/crypto-config/peerOrganizations/insurance.matchedcover.com/{ca,msp,peers/peer0.insurance.matchedcover.com,users/Admin@insurance.matchedcover.com/msp}
    mkdir -p fabric-config/crypto-config/peerOrganizations/reinsurance.matchedcover.com/{ca,msp,peers/peer0.reinsurance.matchedcover.com,users/Admin@reinsurance.matchedcover.com/msp}
fi

# Create channel artifacts
echo -e "${YELLOW}Creating channel artifacts...${NC}"
if command -v configtxgen &> /dev/null; then
    cd fabric-config
    export FABRIC_CFG_PATH=$(pwd)
    
    # Generate genesis block
    configtxgen -profile TwoOrgsApplicationGenesis -outputBlock ./channel-artifacts/genesis.block -channelID system-channel
    
    # Generate channel configuration transaction
    configtxgen -profile TwoOrgsApplicationGenesis -outputCreateChannelTx ./channel-artifacts/insurance-channel.tx -channelID insurance-channel
    
    # Generate anchor peer transactions
    configtxgen -profile TwoOrgsApplicationGenesis -outputAnchorPeersUpdate ./channel-artifacts/InsuranceMSPanchors.tx -channelID insurance-channel -asOrg InsuranceMSP
    configtxgen -profile TwoOrgsApplicationGenesis -outputAnchorPeersUpdate ./channel-artifacts/ReinsuranceMSPanchors.tx -channelID insurance-channel -asOrg ReinsuranceMSP
    
    cd ..
else
    echo -e "${RED}Warning: configtxgen not found. Channel artifacts will be created during runtime.${NC}"
fi

# Create network management scripts
echo -e "${YELLOW}Creating network management scripts...${NC}"

# Network start script
cat > fabric-config/scripts/start-network.sh << 'EOF'
#!/bin/bash
set -e

echo "Starting MatchedCover Insurance Fabric Network..."

# Start the network
docker-compose -f ../docker/docker-compose-fabric.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Create channel
echo "Creating insurance channel..."
docker exec cli peer channel create -o orderer.matchedcover.com:7050 -c insurance-channel -f ./channel-artifacts/insurance-channel.tx --outputBlock ./channel-artifacts/insurance-channel.block --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/matchedcover.com/orderers/orderer.matchedcover.com/msp/tlscacerts/tlsca.matchedcover.com-cert.pem || true

# Join Insurance peer to channel
echo "Joining Insurance peer to channel..."
docker exec cli peer channel join -b ./channel-artifacts/insurance-channel.block

# Join Reinsurance peer to channel
echo "Joining Reinsurance peer to channel..."
docker exec -e CORE_PEER_LOCALMSPID=ReinsuranceMSP -e CORE_PEER_ADDRESS=peer0.reinsurance.matchedcover.com:9051 -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/reinsurance.matchedcover.com/users/Admin@reinsurance.matchedcover.com/msp -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/reinsurance.matchedcover.com/peers/peer0.reinsurance.matchedcover.com/tls/ca.crt cli peer channel join -b ./channel-artifacts/insurance-channel.block

echo "MatchedCover Insurance Fabric Network is ready!"
echo "Insurance peer: localhost:7051"
echo "Reinsurance peer: localhost:9051"
echo "Orderer: localhost:7050"
EOF

# Network stop script
cat > fabric-config/scripts/stop-network.sh << 'EOF'
#!/bin/bash
set -e

echo "Stopping MatchedCover Insurance Fabric Network..."

# Stop and remove containers
docker-compose -f ../docker/docker-compose-fabric.yml down -v

# Remove generated artifacts (optional)
# rm -rf channel-artifacts/*

echo "Network stopped and cleaned up."
EOF

# Deploy chaincode script
cat > fabric-config/scripts/deploy-chaincode.sh << 'EOF'
#!/bin/bash
set -e

CHAINCODE_NAME=${1:-insurance-chaincode}
CHAINCODE_VERSION=${2:-1.0}
CHAINCODE_PATH=${3:-../src/blockchain/chaincode}

echo "Deploying chaincode: $CHAINCODE_NAME v$CHAINCODE_VERSION"

# Package chaincode
echo "Packaging chaincode..."
docker exec cli peer lifecycle chaincode package ${CHAINCODE_NAME}.tar.gz --path ${CHAINCODE_PATH} --lang node --label ${CHAINCODE_NAME}_${CHAINCODE_VERSION}

# Install on Insurance peer
echo "Installing chaincode on Insurance peer..."
docker exec cli peer lifecycle chaincode install ${CHAINCODE_NAME}.tar.gz

# Install on Reinsurance peer
echo "Installing chaincode on Reinsurance peer..."
docker exec -e CORE_PEER_LOCALMSPID=ReinsuranceMSP -e CORE_PEER_ADDRESS=peer0.reinsurance.matchedcover.com:9051 -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/reinsurance.matchedcover.com/users/Admin@reinsurance.matchedcover.com/msp -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/reinsurance.matchedcover.com/peers/peer0.reinsurance.matchedcover.com/tls/ca.crt cli peer lifecycle chaincode install ${CHAINCODE_NAME}.tar.gz

# Get package ID
PACKAGE_ID=$(docker exec cli peer lifecycle chaincode queryinstalled --output json | jq -r ".installed_chaincodes[0].package_id")

# Approve chaincode for Insurance
echo "Approving chaincode for Insurance..."
docker exec cli peer lifecycle chaincode approveformyorg -o orderer.matchedcover.com:7050 --ordererTLSHostnameOverride orderer.matchedcover.com --channelID insurance-channel --name ${CHAINCODE_NAME} --version ${CHAINCODE_VERSION} --package-id $PACKAGE_ID --sequence 1 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/matchedcover.com/orderers/orderer.matchedcover.com/msp/tlscacerts/tlsca.matchedcover.com-cert.pem

# Approve chaincode for Reinsurance
echo "Approving chaincode for Reinsurance..."
docker exec -e CORE_PEER_LOCALMSPID=ReinsuranceMSP -e CORE_PEER_ADDRESS=peer0.reinsurance.matchedcover.com:9051 -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/reinsurance.matchedcover.com/users/Admin@reinsurance.matchedcover.com/msp -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/reinsurance.matchedcover.com/peers/peer0.reinsurance.matchedcover.com/tls/ca.crt cli peer lifecycle chaincode approveformyorg -o orderer.matchedcover.com:7050 --ordererTLSHostnameOverride orderer.matchedcover.com --channelID insurance-channel --name ${CHAINCODE_NAME} --version ${CHAINCODE_VERSION} --package-id $PACKAGE_ID --sequence 1 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/matchedcover.com/orderers/orderer.matchedcover.com/msp/tlscacerts/tlsca.matchedcover.com-cert.pem

# Commit chaincode
echo "Committing chaincode..."
docker exec cli peer lifecycle chaincode commit -o orderer.matchedcover.com:7050 --ordererTLSHostnameOverride orderer.matchedcover.com --channelID insurance-channel --name ${CHAINCODE_NAME} --version ${CHAINCODE_VERSION} --sequence 1 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/matchedcover.com/orderers/orderer.matchedcover.com/msp/tlscacerts/tlsca.matchedcover.com-cert.pem --peerAddresses peer0.insurance.matchedcover.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/insurance.matchedcover.com/peers/peer0.insurance.matchedcover.com/tls/ca.crt --peerAddresses peer0.reinsurance.matchedcover.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/reinsurance.matchedcover.com/peers/peer0.reinsurance.matchedcover.com/tls/ca.crt

echo "Chaincode deployed successfully!"
EOF

# Make scripts executable
chmod +x fabric-config/scripts/*.sh

echo -e "${GREEN}✅ Hyperledger Fabric network setup complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Start the network: ./fabric-config/scripts/start-network.sh"
echo "2. Deploy chaincode: ./fabric-config/scripts/deploy-chaincode.sh"
echo "3. Test the integration: python -m pytest tests/test_blockchain_integration.py"
echo ""
echo -e "${YELLOW}Network endpoints:${NC}"
echo "- Insurance Peer: localhost:7051"
echo "- Reinsurance Peer: localhost:9051"
echo "- Orderer: localhost:7050"
echo "- Insurance CA: localhost:7054"
echo "- Reinsurance CA: localhost:8054"
